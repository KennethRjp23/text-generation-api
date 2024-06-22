from fastapi import FastAPI, HTTPException  # FastAPI for building API endpoints, HHTPException for handling HTTP errors
from transformers import pipeline           # Pipeline from Hugging Face Transformer library for text generation
from cassandra.cluster import Cluster       # Cluster from Cassandra driver for connecting to Cassandra database
from pydantic import BaseModel              # Model to receive request bodies
from dotenv import load_dotenv              # Load environment variables
import uuid                                 # Handle UUID 
import redis                                # Redis client for caching
import os

# Create FastAPI instance
app = FastAPI()

load_dotenv()

class PromptRequest(BaseModel):
    prompt: str

# Initialize text generation pipeline with GPT-2 model
generator = pipeline('text-generation', model='gpt2')

# Connect to Cassandra Cluster and select keyspace
cluster = Cluster([os.getenv('CASSANDRA_HOST')]) # Cassandra host(s)
session = cluster.connect('textgen')  # Connect to 'textgen' keyspace in Cassandra

# Connect to Redis cache
cache = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379, db=0)

# Define API endpoint for text generation
@app.post("/generate/")
async def generate_text(request:PromptRequest):
    # Check if prompt is cached in Redis
    cached_response = cache.get(request.prompt)
    if cached_response:
        return{"text": cached_response.decode('utf-8')} # Return cached response if found
    
    # Generate text using GPT-2 model    
    result = generator(request.prompt, max_length=50)[0]['generated_text']
    # Generate a UUID
    newID = uuid.uuid4()
    # Store generated text in Cassandra database
    session.execute(
        """
        INSERT INTO generated_text (id, prompt, text)
        VALUES (%s, %s, %s)
        """, (newID, request.prompt, result)
    )

    # Cache generated text in Redis
    cache.set(request.prompt, result)

    # Return generated text
    return {"text": result}

# Define root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Text Generation API"}
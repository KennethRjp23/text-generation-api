from fastapi import FastAPI, HTTPException  # FastAPI for building API endpoints, HHTPException for handling HTTP errors
from transformers import pipeline           # Pipeline from Hugging Face Transformer library for text generation
from cassandra.cluster import Cluster       # Cluster from Cassandra driver for connecting to Cassandra database
import redis                                # Redis client for caching

# Create FastAPI instance
app = FastAPI()

# Initialize text generation pipeline with GPT-2 model
generator = pipeline('text-generation', model='gpt2')

# Connect to Cassandra Cluster and select keyspace
cluster = Cluster(['cassandra-host']) # Cassandra host(s)
session = cluster.connect('textgen')  # Connect to 'textgen' keyspace in Cassandra

# Connect to Redis cache
cache = redis.Redis(host='redis-host')

# Define API endpoint for text generation
@app.post("/generate/")
async def generate_text(prompt:str):
    # Check if prompt is cached in Redis
    cached_response = cache.get(prompt)
    if cached_response:
        return{"text": cached_response.decode('utf-8')} # Return cached response if found
    
    # Generate text using GPT-2 model
    result = generator(prompt, max_length=50)[0]['generated_text']

    # Store generated text in Cassandra database
    session.execute(
        """
        INSERT INTO generated_text (prompt, text)
        VALUES (%s, %s)
        """, (prompt, result)
    )

    # Cache generated text in Redis
    cache.set(prompt, result)

    # Return generated text
    return {"text": result}

# Define root endpoint
@app.get("/")
async def read_root():
    return {"message": "Weclome to the Text Generation API"}
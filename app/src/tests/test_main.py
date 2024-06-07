from fastapi.testclient import TestClient # TestClient for testing FastAPI endpoints
from main import app                      # Import the FastAPI instance from main.py

# Create a TestClient instance to test FastAPI endpoints
client = TestClient(app)

# Define test functions for the API endpoints

# Test the root endpoint "/"
def test_read_root():
    # Send a GET request to the root endpoint
    response = client.get("/")
    # Assert that response status code is 200 (OK)
    assert response.status_code == 200
    # Assert that the response JSON matches the expected message
    assert response.json() == {"message": "Welcome to the Text Generation API"}

def text_generate_text():
    # Send a POST request to the "/generate/" endpoint with a prompt
    response = client.post("/generate/", json={"prompt": "Hello, world"})
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    # Asser that the response contains the generated text
    assert "text" in response.json()
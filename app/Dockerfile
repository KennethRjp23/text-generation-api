# Use the official Python 3.9 slim image as base
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirments.txt file from the host into the container at /app
COPY requirements.txt .

# Install the Python dependencies listed in requirements.txt
RUN pip install -r requirements.txt

# Copy the contents of the src/ direcoty from the host into the container at /app
COPY src/ . 

# Define the command to run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
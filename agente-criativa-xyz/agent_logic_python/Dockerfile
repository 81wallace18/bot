# Use Python 3.11 (requerido pelo CrewAI)
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip and install Python packages
RUN pip install -r requirements.txt

    
# Copy the rest of the application code into the container
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the uvicorn server when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

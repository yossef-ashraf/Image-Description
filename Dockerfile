FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Increase timeout and verbosity for pip
RUN pip install --no-cache-dir --timeout=300 --verbose -r requirements.txt

# Copy the rest of the application
COPY app/ .

# Create upload directory
RUN mkdir -p uploads

# Download models during build
RUN python models/download_model.py

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
# Use the official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for PyArrow, Pandas, and others
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        gcc \
        g++ \
        make \
        curl \
        git \
        && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -e .

# Optional: run tests or training (you can comment this out)
# CMD ["python", "train.py"]

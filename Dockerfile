# Use a lightweight Python image
FROM python:slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends libgomp1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Optional: run training (only if you really need to)
# RUN python pipeline/training_pipeline.py

# Expose app port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]


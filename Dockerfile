# Dockerfile for HK Visa Appointment Checker
FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY *.py .
COPY config.example.env .

# Create volume mount point for config
VOLUME ["/app/config"]

# Run the application
CMD ["python", "main.py"]

# Use Python 3.8 base image
FROM python:3.8

# Set working directory inside container
WORKDIR /app

# Copy requirements file first (for caching layers)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy handler.py into container
COPY handler.py .

# Default command to run your handler
CMD ["python", "handler.py"]
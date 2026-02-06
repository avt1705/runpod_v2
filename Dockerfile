FROM python:3.10-slim

# Install system dependencies needed for CUDA/Graphics
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
# We update pip to ensure it can find the latest torch 2.4+
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY handler.py .

CMD ["python", "-u", "handler.py"]

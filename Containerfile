FROM docker.io/python:3.12-slim

WORKDIR /data

# Install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

# Copy application
COPY download.py /app/download.py

# Set entrypoint
ENTRYPOINT ["python", "/app/download.py"]

FROM ubuntu:24.04

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt --break-system-packages

# Copy Python script to /usr/local/bin so it survives volume mounts
COPY picopaper.py /usr/local/bin/picopaper.py

# Set working directory
WORKDIR /app

# Add /app to Python path so it can find config.py from mounted volume
ENV PYTHONPATH=/app

# Run as root to allow writing to mounted volumes
# (The mounted volume will have host user permissions)

# Generate the site on container start
CMD ["python3", "/usr/local/bin/picopaper.py"]

# Copy config.py to /app
COPY config.py /app/config.py

# Copy other necessary files
COPY items /app/items
COPY theme /app/theme
COPY static /app/static

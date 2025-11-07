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

# Copy configuration file
COPY config.py /app/config.py

# Copy content directories
COPY items /app/items
COPY theme /app/theme
COPY static /app/static
COPY images /app/images

# Set working directory
WORKDIR /app

# Add /app to Python path so it can find config.py
ENV PYTHONPATH=/app

# Expose port 8000 only
EXPOSE 8000

# Generate the site and serve it ONLY on port 8000
# --bind 0.0.0.0 listens on all interfaces but only on port 8000
# This prevents conflicts with other containers on different ports
CMD ["bash", "-c", "python3 /usr/local/bin/picopaper.py && exec python3 -m http.server 8000 --directory /app/output --bind 0.0.0.0"]

FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt --break-system-packages

COPY picopaper.py /usr/local/bin/picopaper.py
COPY config.py /app/config.py
COPY items /app/items
COPY theme /app/theme
COPY static /app/static

WORKDIR /app
ENV PYTHONPATH=/app

EXPOSE 8000

# Create startup script that generates site and keeps server running
RUN echo '#!/bin/bash\nset -e\necho "Generating site..."\npython3 /usr/local/bin/picopaper.py\necho "Starting HTTP server on port 8000..."\nexec python3 -m http.server 8000 --directory /app/output --bind 0.0.0.0' > /startup.sh && chmod +x /startup.sh

CMD ["/startup.sh"]

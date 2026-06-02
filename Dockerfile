# Dockerfile untuk stack digitalentappython
# Sesuai CLAUDE.md stack: python 3, terminal, nano, mysql client
# Image kecil berbasis python:3.11-slim

FROM python:3.11-slim

LABEL maintainer="digitalentappython" \
      description="Latihan Python & Data Science - terminal interaktif dengan MySQL"

# Install tools sesuai stack CLAUDE.md: nano, mysql client, curl
# apt cleanup di akhir agar image tetap kecil
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nano \
        default-mysql-client \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory di dalam container
WORKDIR /workspace

# Copy requirements dulu agar cache Docker optimal
COPY requirements.txt .

# Install dependency Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code aplikasi
COPY app/ ./app/
COPY sql/ ./sql/

# Default command: sleep infinity supaya container tetap hidup
# User bisa masuk lewat: docker compose exec python bash
CMD ["tail", "-f", "/dev/null"]

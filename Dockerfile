FROM debian:bullseye-slim

# Installazione dipendenze di sistema
RUN apt-get update && apt-get install -y \
    imapsync \
    python3 \
    python3-pip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Configurazione directory applicazione
WORKDIR /app

# Copia file richiesti
COPY requirements.txt ./
COPY scripts/ ./scripts/
COPY config/ ./config/

# Installazione dipendenze Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Imposta permessi script
RUN chmod +x ./scripts/entrypoint.sh ./scripts/sync_emails.py

# Script di entrata
ENTRYPOINT ["./scripts/entrypoint.sh"]
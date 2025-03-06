FROM debian:bullseye-slim

# Installazione dipendenze di sistema e strumenti necessari
RUN apt-get update && apt-get install -y \
    libauthen-ntlm-perl \
    libcgi-pm-perl \
    libcrypt-openssl-rsa-perl \
    libdata-uniqid-perl \
    libencode-imaputf7-perl \
    libfile-copy-recursive-perl \
    libfile-tail-perl \
    libio-socket-inet6-perl \
    libio-socket-ssl-perl \
    libio-tee-perl \
    libhtml-parser-perl \
    libjson-webtoken-perl \
    libmail-imapclient-perl \
    libparse-recdescent-perl \
    libproc-processtable-perl \
    libmodule-scandeps-perl \
    libreadonly-perl \
    libregexp-common-perl \
    libsys-meminfo-perl \
    libterm-readkey-perl \
    libtest-mockobject-perl \
    libunicode-string-perl \
    liburi-perl \
    libwww-perl \
    libnet-server-perl \
    make \
    time \
    cpanminus \
    wget \
    curl \
    ca-certificates \
    perl \
    python3 \
    python3-pip \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Scarica imapsync direttamente da GitHub
RUN curl -L https://github.com/imapsync/imapsync/raw/refs/heads/master/imapsync -o /usr/local/bin/imapsync \
    && chmod +x /usr/local/bin/imapsync

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
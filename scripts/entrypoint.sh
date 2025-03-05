#!/bin/bash

# Abilita mode debug e gestione errori
set -e
set -o pipefail

# Configurazione logging
LOG_DIR="/app/logs"
mkdir -p "$LOG_DIR"

# Avvio script di sincronizzazione Python
python3 /app/scripts/sync_emails.py
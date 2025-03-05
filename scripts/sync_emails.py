#!/usr/bin/env python3
import os
import yaml
import logging
import schedule
import time
import subprocess
from datetime import datetime

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/email_sync.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_config():
    """Carica configurazione da file YAML"""
    try:
        with open('/app/config/email_sync.yaml', 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Errore caricamento configurazione: {e}")
        raise

def sync_email(config):
    """Esegue sincronizzazione per ogni account email"""
    for account in config.get('accounts', []):
        try:
            # Costruzione comando imapsync
            cmd = [
                'imapsync',
                '--host1', account['source']['host'],
                '--user1', account['source']['username'],
                '--password1', account['source']['password'],
                '--host2', account['destination']['host'],
                '--user2', account['destination']['username'],
                '--password2', account['destination']['password']
            ]

            # Aggiungi opzioni aggiuntive
            additional_options = account.get('options', {})
            for option, value in additional_options.items():
                cmd.extend([f'--{option}', str(value)])

            # Esecuzione sincronizzazione
            logger.info(f"Sincronizzazione account: {account['source']['username']}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Sincronizzazione completata per {account['source']['username']}")
            else:
                logger.error(f"Errore sincronizzazione {account['source']['username']}: {result.stderr}")

        except Exception as e:
            logger.error(f"Errore durante sincronizzazione: {e}")

def main():
    """Funzione principale di schedulazione"""
    try:
        config = load_config()
        
        # Configurazione schedulazione
        schedule_config = config.get('schedule', {})
        interval = schedule_config.get('interval')
        time_of_day = schedule_config.get('time')

        # Se non è configurata la schedulazione, esegui immediatamente
        if not interval or not time_of_day:
            logger.info("Nessuna schedulazione configurata. Esecuzione immediata.")
            sync_email(config)
            return

        # Imposta schedulazione
        if interval == 'hourly':
            schedule.every().hour.do(sync_email, config)
        elif interval == 'daily':
            schedule.every().day.at(time_of_day).do(sync_email, config)
        elif interval == 'weekly':
            schedule.every().week.at(time_of_day).do(sync_email, config)
        
        logger.info(f"Sincronizzazione pianificata: {interval} alle {time_of_day}")

        # Loop di esecuzione
        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        logger.error(f"Errore durante esecuzione: {e}")
        raise

if __name__ == "__main__":
    main()
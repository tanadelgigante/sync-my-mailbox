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
            source_user = account['source']['username']
            dest_user = account['destination']['username']
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"/app/logs/imapsync_{source_user.replace('@', '_')}_{timestamp}.log"
            
            # Costruzione comando imapsync
            cmd = [
                'imapsync',
                '--host1', account['source']['host'],
                '--user1', source_user,
                '--password1', account['source']['password'],
                '--host2', account['destination']['host'],
                '--user2', dest_user,
                '--password2', account['destination']['password'],
                '--nolog'  # Disabilita il log interno di imapsync poiché gestiremo l'output manualmente
            ]

            # Aggiungi opzioni aggiuntive
            additional_options = account.get('options', {})
            for option, value in additional_options.items():
                cmd.extend([f'--{option}', str(value)])

            # Esecuzione sincronizzazione con tee per salvare l'output
            logger.info(f"Sincronizzazione account: {source_user}")
            
            # Apri il file di log per imapsync
            with open(log_filename, 'w') as log_file:
                # Esegui il processo
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                
                # Processa l'output in tempo reale
                for line in process.stdout:
                    # Scrivi nel file di log
                    log_file.write(line)
                    # Scrivi nei log di applicazione (limitato a linee significative)
                    line = line.strip()
                    if "ETA:" not in line and line:  # Ignora le linee con ETA che sono molto verbose
                        logger.info(f"IMAPSYNC {source_user}: {line}")
                
                # Aspetta che il processo termini
                return_code = process.wait()
                
                if return_code == 0:
                    logger.info(f"Sincronizzazione completata con successo per {source_user}")
                else:
                    logger.error(f"Errore nella sincronizzazione di {source_user} (codice: {return_code})")
                
                logger.info(f"Log dettagliato salvato in: {log_filename}")

        except Exception as e:
            logger.error(f"Errore durante sincronizzazione di {source_user}: {e}")

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
            
            # Exit dopo l'esecuzione se non c'è schedulazione
            logger.info("Sincronizzazione completata. Uscita.")
            return
        
        # Esegui una sincronizzazione all'avvio
        logger.info("Esecuzione sincronizzazione all'avvio...")
        sync_email(config)
        
        # Imposta schedulazione
        if interval == 'hourly':
            schedule.every().hour.do(sync_email, config)
        elif interval == 'daily':
            schedule.every().day.at(time_of_day).do(sync_email, config)
        elif interval == 'weekly':
            schedule.every().week.at(time_of_day).do(sync_email, config)
        elif interval == 'custom' and 'minutes' in schedule_config:
            minutes = int(schedule_config['minutes'])
            schedule.every(minutes).minutes.do(sync_email, config)
        
        logger.info(f"Sincronizzazione pianificata: {interval}" + 
                   (f" alle {time_of_day}" if time_of_day else "") +
                   (f" ogni {schedule_config.get('minutes')} minuti" if interval == 'custom' else ""))

        # Loop di esecuzione
        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        logger.error(f"Errore durante esecuzione: {e}")
        raise

if __name__ == "__main__":
    main()
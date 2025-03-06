# SyncMyMailbox

## Descrizione
SyncMyMailbox è un container Docker per la sincronizzazione automatizzata di caselle email multiple utilizzando imapsync. Basato sul progetto [imapsync](https://github.com/imapsync/imapsync).

## Caratteristiche
- Sincronizzazione configurabile di multiple caselle email
- Schedulazione flessibile (oraria, giornaliera, settimanale)
- Supporto per Gmail, Outlook e altri provider IMAP
- Logging dettagliato
- Configurazione tramite file YAML

## Requisiti
- Docker
- Docker Compose

## Configurazione

### Configurazione Email (config.yml)
```yaml
accounts:
  # Configurazione Gmail
  - source:
      host: imap.gmail.com
      username: email1@gmail.com
      password: app_password_gmail
    destination:
      host: localhost
      username: local_user1
      password: local_password
    options:
      ssl1: true        # Usa SSL per la connessione sorgente
      ssl2: true        # Usa SSL per la connessione destinazione
      useheader: "Message-ID"  # Identificatore univoco per email Gmail
      skiptomsg: 0      # Inizia dalla prima email
      nosyncacls: true  # Non sincronizzare gli ACL
      syncinternaldates: true  # Sincronizza le date interne
      skipsize: true    # Salta il controllo dimensioni
      nofoldersizes: true  # Non recuperare le dimensioni delle cartelle
      allowsizemismatch: true  # Permetti differenze di dimensione

  # Configurazione Outlook/Office365
  - source:
      host: outlook.office365.com
      username: email2@outlook.com
      password: app_password_outlook
    destination:
      host: localhost
      username: local_user2
      password: local_password
    options:
      ssl1: true        # Usa SSL per la connessione sorgente
      ssl2: true        # Usa SSL per la connessione destinazione
      automap: true     # Mappa automaticamente le cartelle
      skipsize: true    # Salta il controllo dimensioni
      useheader: "Message-ID"  # Identificatore univoco
      syncinternaldates: true  # Sincronizza le date interne
      nofoldersizes: true  # Non recuperare le dimensioni delle cartelle
      allowsizemismatch: true  # Permetti differenze di dimensione

  # Esempio configurazione per Dovecot (server IMAP generico)
  - source:
      host: mail.example.com
      username: email3@example.com
      password: password3
    destination:
      host: localhost
      username: local_user3
      password: local_password
    options:
      port1: 993        # Porta IMAP (default 143)
      port2: 143        # Porta IMAP locale
      ssl1: true        # Usa SSL per la connessione sorgente
      tls2: true        # Usa TLS per la connessione destinazione
      subfolder2: "Backup"  # Metti le email in una sottocartella
      exclude: "Trash|Spam"  # Escludi queste cartelle
      maxsize: 50000000  # Dimensione massima email (50MB)
      maxage: 3650      # Massima età email in giorni (10 anni)
```

### Configurazione Schedule (schedule.yml)
```yaml
schedule:
  interval: custom  # Opzioni: hourly, daily, weekly, custom
  minutes: 180      # Ogni 3 ore (solo se interval è 'custom')
  time: '02:00'     # Ora di sincronizzazione (per daily e weekly)
```

## Avvio

```bash
docker-compose up -d
```

## Logging
I log vengono salvati in:
- `/logs/sync_YYYYMMDD.log` - Log delle sincronizzazioni
- `/logs/error_YYYYMMDD.log` - Log degli errori

## Opzioni Avanzate

### SSL/TLS
- `ssl: true` - Usa connessione SSL/TLS
- `ssl_verify: false` - Disabilita verifica certificato

### Filtri
- `exclude: ["folder1", "folder2"]` - Esclude cartelle
- `include: ["folder1", "folder2"]` - Sincronizza solo cartelle specifiche

### Eliminazione
- `delete: true` - Elimina email nella destinazione se eliminate nella sorgente
- `delete_after: 30` - Elimina email più vecchie di X giorni

## Sicurezza
- Si raccomanda l'uso di password app-specific per Gmail e altri servizi
- Le password vengono gestite in modo sicuro tramite variabili d'ambiente
- Supporto per autenticazione OAuth2 (configurazione aggiuntiva richiesta)

## Credits
Questo progetto utilizza [imapsync](https://github.com/imapsync/imapsync), uno strumento potente per la sincronizzazione IMAP creato da Gilles LAMIRAL. Per maggiori informazioni su imapsync, visita la [documentazione ufficiale](https://imapsync.lamiral.info/).

## Licenza
GNU General Public License v3.0 - Vedi [LICENSE](LICENSE)

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
  - name: "Account1"
    source:
      host: "imap.gmail.com"
      port: 993
      user: "source@gmail.com"
      password: "your_password"
      ssl: true
    destination:
      host: "outlook.office365.com"
      port: 993
      user: "dest@outlook.com"
      password: "your_password"
      ssl: true
    options:
      delete: false
      subfolder: "Archive"
      exclude: ["Spam", "Trash"]
```

### Configurazione Schedule (schedule.yml)
```yaml
schedules:
  - name: "Account1"
    frequency: "daily"
    time: "02:00"
    days: ["monday", "wednesday", "friday"]
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

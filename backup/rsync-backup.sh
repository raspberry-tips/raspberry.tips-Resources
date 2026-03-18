#!/bin/bash
# Automatisches rsync Backup Script für den Raspberry Pi
# Tutorial: https://raspberry.tips/raspberrypi-tutorials/raspberry-pi-datensicherung-erstellen
# Verwendung: sudo bash rsync-backup.sh
# Für automatischen Start: in crontab -e eintragen (siehe crontab-example.txt)

BACKUP_DEST="/media/pi/BACKUP"   # Zielverzeichnis anpassen
LOG_FILE="/var/log/rpi-backup.log"
DATE=$(date +%Y-%m-%d_%H-%M)

echo "[$DATE] Starte Backup nach $BACKUP_DEST" >> "$LOG_FILE"

# Prüfen ob Zielmedium eingehängt ist
if ! mountpoint -q "$BACKUP_DEST"; then
    echo "[$DATE] FEHLER: $BACKUP_DEST ist nicht eingehängt!" >> "$LOG_FILE"
    exit 1
fi

# Backup durchführen
rsync -avz --delete /home/ "$BACKUP_DEST/home/" >> "$LOG_FILE" 2>&1
rsync -avz --delete /etc/ "$BACKUP_DEST/etc/" >> "$LOG_FILE" 2>&1

echo "[$DATE] Backup abgeschlossen." >> "$LOG_FILE"

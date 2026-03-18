# Raspberry Pi Backup Scripts

Scripts für automatische Datensicherung des Raspberry Pi.

**Vollständiges Tutorial:** [raspberry.tips → Raspberry Pi Backup erstellen](https://raspberry.tips/raspberrypi-tutorials/raspberry-pi-datensicherung-erstellen)

## Dateien

- `rpi-clone-setup.sh` – rpi-clone (geerlingguy Fork) installieren
- `rsync-backup.sh` – automatisches rsync Backup auf USB oder NAS
- `crontab-example.txt` – Beispiel-Crontab für automatische Backups

## Wichtig für Bookworm / Pi 5

Das originale rpi-clone (billw2) funktioniert **nicht** korrekt unter Raspberry Pi OS Bookworm.
Verwendet den **geerlingguy Fork** (in `rpi-clone-setup.sh` enthalten).

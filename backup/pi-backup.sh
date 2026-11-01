#!/bin/bash
# Back up /home and /etc to the drive mounted at /mnt/backup
# Guide (DE): https://raspberry.tips/raspberrypi-tutorials/raspberry-pi-datensicherung-erstellen
# Guide (EN): https://raspberry.tips/en/raspberrypi-tutorials/raspberry-pi-backup-guide
# Install: sudo cp pi-backup.sh /usr/local/bin/ && sudo chmod +x /usr/local/bin/pi-backup.sh
# The target must be formatted as ext4 (FAT32/exFAT lose Linux permissions and symlinks).
TARGET=/mnt/backup

# Stop if the drive is not mounted, otherwise rsync would fill the system drive
if ! mountpoint -q "$TARGET"; then
    echo "$(date): $TARGET is not mounted, backup skipped" >&2
    exit 1
fi

rsync -a --delete /home/ "$TARGET/home/"
rsync -a --delete /etc/ "$TARGET/etc/"
echo "$(date): backup finished"

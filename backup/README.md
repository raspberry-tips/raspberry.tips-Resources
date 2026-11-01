# Raspberry Pi Backup Scripts

Scripts from the raspberry.tips backup guide:

- DE: [Raspberry Pi Backup erstellen](https://raspberry.tips/raspberrypi-tutorials/raspberry-pi-datensicherung-erstellen)
- EN: [How to Back Up a Raspberry Pi](https://raspberry.tips/en/raspberrypi-tutorials/raspberry-pi-backup-guide)

## Files

- `rpi-clone-setup.sh` – installs rpi-clone (Jeff Geerling's fork) and prints the common commands
- `pi-backup.sh` – rsync backup of `/home` and `/etc` to a drive mounted at `/mnt/backup`; skips the run if the drive is not mounted
- `crontab-example.txt` – cron line for a nightly run

## Notes

- Format the backup drive as **ext4**. On FAT32/exFAT, rsync loses owners, permissions and symlinks (`/etc/shadow` would become world-readable).
- `--delete` makes the target a mirror: files deleted on the Pi disappear from the backup on the next run. For several versions, use raspiBackup or shrink-backup (see the guide).
- Use the maintained rpi-clone fork (geerlingguy); the original (billw2) has not been maintained since 2020.

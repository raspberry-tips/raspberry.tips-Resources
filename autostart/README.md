# Raspberry Pi Autostart – systemd Service Templates

Fertige systemd Service-Templates für den Raspberry Pi Autostart.

**Vollständiges Tutorial:** [raspberry.tips → Autostart von Skripten und Programmen einrichten](https://raspberry.tips/raspberrypi-einsteiger/raspberry-pi-autostart-von-skripten-und-programmen-einrichten)

## Verwendung

```bash
# Template nach /etc/systemd/system/ kopieren und anpassen
sudo cp python-script.service /etc/systemd/system/meinskript.service
sudo nano /etc/systemd/system/meinskript.service

# Service aktivieren und starten
sudo systemctl daemon-reload
sudo systemctl enable meinskript.service
sudo systemctl start meinskript.service

# Status prüfen
sudo systemctl status meinskript.service
sudo journalctl -u meinskript.service
```

# Raspberry Pi Autostart – systemd Service Templates

Fertige systemd Service-Templates für den Raspberry Pi Autostart.

**Vollständiges Tutorial:** [raspberry.tips → Autostart von Skripten und Programmen einrichten](https://raspberry.tips/raspberrypi-einsteiger/raspberry-pi-autostart-von-skripten-und-programmen-einrichten)

## Verwendung

```bash
# Template nach /etc/systemd/system/ kopieren und anpassen
# (User= und Pfade: "benutzer" durch euren Benutzernamen ersetzen, siehe whoami)
sudo cp python-script.service /etc/systemd/system/meinskript.service
sudo nano /etc/systemd/system/meinskript.service

# Service aktivieren und sofort starten
sudo systemctl daemon-reload
sudo systemctl enable --now meinskript.service

# Status und Ausgaben prüfen
systemctl status meinskript.service
journalctl -u meinskript.service
```

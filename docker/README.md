# Docker Compose Files für den Raspberry Pi

Fertige Docker Compose Konfigurationen für populäre Heimserver-Dienste.

**Vollständiges Tutorial:** [raspberry.tips → Docker auf dem Raspberry Pi installieren](https://raspberry.tips/raspberrypi-tutorials/docker-raspberry-pi-installieren)

## Dienste

| Datei | Dienst | Tutorial |
|---|---|---|
| `pihole.yml` | Pi-hole Werbeblocker | [→](https://raspberry.tips/raspberrypi-tutorials/pi-hole-einrichten-netzwerkweiter-werbeblocker) |
| `nextcloud.yml` | Nextcloud AIO | [→](https://raspberry.tips/raspberrypi-tutorials/nextcloud-raspberry-pi-installieren) |
| `homeassistant.yml` | Home Assistant | [→](https://raspberry.tips/raspberrypi-tutorials/home-assistant-raspberry-pi-installieren) |
| `ollama.yml` | Ollama + Open WebUI | [→](https://raspberry.tips/raspberrypi-tutorials/ollama-raspberry-pi-5) |

## Verwendung

```bash
docker compose -f pihole.yml up -d
```

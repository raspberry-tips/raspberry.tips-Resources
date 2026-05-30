# RFID RC522 am Raspberry Pi 5

Python-Code aus dem Artikel [RFID RC522 am Raspberry Pi 5 auslesen](https://raspberry.tips/rfid-rc522-raspberry-pi-5) auf raspberry.tips.

## Voraussetzungen

SPI aktivieren:
```bash
sudo raspi-config  # Interface Options -> I4 SPI -> Yes
sudo reboot
```

Pakete installieren:
```bash
sudo apt update
sudo apt install python3-spidev python3-libgpiod -y
```

## Nutzung

```bash
git clone https://github.com/raspberry-tips/raspberry.tips-Resources.git
cd raspberry.tips-Resources/rfid-rc522
python3 rfid_lesen.py
```

## Dateien

| Datei | Beschreibung |
|---|---|
| `mfrc522_pi5.py` | MFRC522-Klasse fuer Pi 5 (spidev + gpiod, kein RPi.GPIO) |
| `rfid_lesen.py` | UIDs von RFID-Tags auslesen |

## Verkabelung RC522 an Raspberry Pi 5

| RC522 Pin | Pi 5 Pin | GPIO (BCM) |
|---|---|---|
| VCC  | Pin 1  | 3,3 V   |
| GND  | Pin 6  | Ground  |
| MOSI | Pin 19 | GPIO 10 |
| MISO | Pin 21 | GPIO 9  |
| SCK  | Pin 23 | GPIO 11 |
| SDA  | Pin 24 | GPIO 8  |
| RST  | Pin 22 | GPIO 25 |

Getestet auf Raspberry Pi 5 mit Raspberry Pi OS Bookworm (2025).

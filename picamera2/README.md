# Picamera2 – Raspberry Pi Kamera mit Python steuern

Python-Skripte aus dem Artikel **[Picamera2: Raspberry Pi Kamera mit Python steuern – Fotos, Video, Livestream und OpenCV](https://raspberry.tips/raspberrypi-tutorials/picamera2-raspberry-pi-kamera-python)** auf raspberry.tips (English version: [Picamera2: Control the Raspberry Pi Camera with Python](https://raspberry.tips/en/raspberrypi-tutorials/picamera2-raspberry-pi-camera-python)).

Alle Skripte wurden auf einem Raspberry Pi 3 mit aktuellem Raspberry Pi OS (64-Bit), Picamera2 0.3.37 und einem IMX219-Kameramodul getestet. Die Erklärungen zu jedem Skript – Sensor-Modi, Controls, Encoder, Farbkanäle, Tuning-Dateien – stehen im Artikel.

## Voraussetzungen

Picamera2 ist auf Raspberry Pi OS mit Desktop vorinstalliert. Auf Raspberry Pi OS Lite:

```bash
sudo apt update
sudo apt install -y python3-picamera2 --no-install-recommends
sudo apt install -y python3-opencv        # nur für 07 und 08
```

Kamera prüfen:

```bash
rpicam-hello --list-cameras
```

## Nutzung

```bash
git clone https://github.com/raspberry-tips/raspberry.tips-Resources.git
cd raspberry.tips-Resources/picamera2
python3 01_photo.py
```

Alle Skripte laufen mit dem System-Python, eine virtuelle Umgebung ist nicht nötig. Wer eine braucht, legt sie mit `python3 -m venv --system-site-packages` an, sonst sieht sie die apt-Pakete nicht (Details im Artikel).

## Dateien

| Datei | Beschreibung |
|---|---|
| `01_photo.py` | Ein Foto in voller Sensorauflösung aufnehmen |
| `02_configuration.py` | Sensor-Modi auflisten, Konfiguration mit `main`- und `lores`-Stream |
| `03_controls.py` | Manuelle Belichtung, Weißabgleich-Voreinstellungen, Bildregler |
| `04_transform_noir.py` | Bild um 180° drehen, Tuning-Datei für NoIR-Module laden |
| `05_video.py` | H.264 roh, MP4 mit `PyavOutput`, Clip fester Länge |
| `06_mjpeg_stream.py` | MJPEG-Livestream im Browser (`http://<pi-ip>:8000`) |
| `07_opencv_edges.py` | Bild als NumPy-Array, Canny-Kanten mit OpenCV, RGB/BGR-Falle |
| `08_motion_detection.py` | Bewegungserkennung auf dem `lores`-Stream, Vollbild bei Bewegung |
| `09_timelapse.py` | Zeitraffer mit eingefrorener Belichtung und Weißabgleich |

Getestet auf Raspberry Pi 3 Model B, Raspberry Pi OS 64-Bit (September 2026).

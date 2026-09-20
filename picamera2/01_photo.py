#!/usr/bin/env python3
# Picamera2 example from the raspberry.tips tutorial
# https://raspberry.tips/raspberrypi-tutorials/picamera2-raspberry-pi-kamera-python
# Take a single still image at full sensor resolution.
from picamera2 import Picamera2

picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()
picam2.capture_file("photo.jpg")
picam2.stop()
print("saved: photo.jpg")

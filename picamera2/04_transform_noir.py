#!/usr/bin/env python3
# Picamera2 example from the raspberry.tips tutorial
# https://raspberry.tips/raspberrypi-tutorials/picamera2-raspberry-pi-kamera-python
# Rotate the image by 180 degrees (camera mounted upside down) and load the
# NoIR tuning file for a camera module without an infrared filter.
from libcamera import Transform
from picamera2 import Picamera2

# Use the matching tuning file for NoIR modules: libcamera picks the standard one
# by sensor name (imx219.json) and does not know that yours has no IR filter.
tuning = Picamera2.load_tuning_file("imx219_noir.json")   # imx708_noir.json for the Camera Module 3 NoIR
picam2 = Picamera2(tuning=tuning)

# hflip + vflip = 180 degree rotation, applied to all streams
config = picam2.create_still_configuration(transform=Transform(hflip=1, vflip=1))
picam2.configure(config)
picam2.start()
picam2.capture_file("rotated_noir.jpg")
picam2.stop()

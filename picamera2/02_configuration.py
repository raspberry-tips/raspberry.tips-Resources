#!/usr/bin/env python3
# Picamera2 example from the raspberry.tips tutorial
# https://raspberry.tips/raspberrypi-tutorials/picamera2-raspberry-pi-kamera-python
# List the sensor modes and build a configuration with a main and a lores stream.
from picamera2 import Picamera2

picam2 = Picamera2()

print("Sensor modes:")
for mode in picam2.sensor_modes:
    print(f"  {mode['size']}  {mode['bit_depth']} bit  max {mode['fps']:.1f} fps  crop {mode['crop_limits']}")

config = picam2.create_still_configuration(
    main={"size": (1640, 1232)},
    lores={"size": (320, 240), "format": "YUV420"},
)
picam2.configure(config)
print(picam2.camera_configuration()["main"])
print(picam2.camera_configuration()["lores"])

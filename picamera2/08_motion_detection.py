#!/usr/bin/env python3
# Picamera2 example from the raspberry.tips tutorial
# https://raspberry.tips/raspberrypi-tutorials/picamera2-raspberry-pi-kamera-python
# Simple motion detection on the small lores stream; saves a full-resolution photo on motion.
import time

import numpy as np
from picamera2 import Picamera2

picam2 = Picamera2()
config = picam2.create_still_configuration(
    main={"size": (1640, 1232)},
    lores={"size": (320, 240), "format": "YUV420"},
)
picam2.configure(config)
picam2.start()
time.sleep(1)

# Mean pixel difference that counts as motion. Measure it for your setup: with a static
# scene at roughly 50 lux we saw 2.1-2.6 (sensor noise), waving in front of the camera 15-54.
THRESHOLD = 6.0
previous = None
while True:
    yuv = picam2.capture_array("lores")
    current = yuv[:240, :320].astype(np.int16)   # Y plane = greyscale image
    if previous is not None:
        diff = np.abs(current - previous).mean()
        if diff > THRESHOLD:
            print(f"motion detected (difference {diff:.1f})")
            picam2.capture_file(time.strftime("motion_%Y%m%d_%H%M%S.jpg"))
            time.sleep(2)               # pause so not every frame triggers
    previous = current
    time.sleep(0.1)

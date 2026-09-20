#!/usr/bin/env python3
# Picamera2 example from the raspberry.tips tutorial
# https://raspberry.tips/raspberrypi-tutorials/picamera2-raspberry-pi-kamera-python
# Timelapse with frozen exposure and white balance (no flicker between frames).
# Assemble afterwards:
#   ffmpeg -framerate 24 -i tl_%04d.jpg -c:v libx264 -pix_fmt yuv420p timelapse.mp4
import time

from picamera2 import Picamera2

INTERVAL = 30      # seconds between two frames
FRAMES = 240       # 240 frames = 2 hours, gives 10 s of video at 24 fps

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration(main={"size": (1920, 1440)}))
picam2.start()
time.sleep(2)

# Read the values the automatics settled on and lock them
meta = picam2.capture_metadata()
picam2.set_controls({
    "AeEnable": False, "AwbEnable": False,
    "ExposureTime": meta["ExposureTime"], "AnalogueGain": meta["AnalogueGain"],
    "ColourGains": meta["ColourGains"],
})

for i in range(FRAMES):
    start = time.time()
    picam2.capture_file(f"tl_{i:04d}.jpg")
    time.sleep(max(0, INTERVAL - (time.time() - start)))   # keep the interval, capture time included

picam2.stop()

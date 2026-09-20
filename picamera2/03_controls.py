#!/usr/bin/env python3
# Picamera2 example from the raspberry.tips tutorial
# https://raspberry.tips/raspberrypi-tutorials/picamera2-raspberry-pi-kamera-python
# Camera controls: manual exposure, white balance presets, image adjustments.
import time

from libcamera import controls
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration(main={"size": (1640, 1232)}))
picam2.start()
time.sleep(1)

meta = picam2.capture_metadata()
print(f"auto: {meta['ExposureTime']} us, gain {meta['AnalogueGain']:.2f}, lux {meta['Lux']:.0f}")
picam2.capture_file("auto.jpg")

# Disable auto exposure and set fixed values
picam2.set_controls({"AeEnable": False, "ExposureTime": 10000, "AnalogueGain": 1.0})
time.sleep(0.5)   # wait a few frames until the new values take effect
picam2.capture_file("manual_10ms.jpg")

picam2.set_controls({"ExposureTime": 60000, "AnalogueGain": 4.0})
time.sleep(0.5)
picam2.capture_file("manual_60ms.jpg")

# White balance: preset (Auto, Tungsten, Fluorescent, Indoor, Daylight, Cloudy) ...
picam2.set_controls({"AeEnable": True, "AwbMode": controls.AwbModeEnum.Tungsten})
time.sleep(0.5)
picam2.capture_file("awb_tungsten.jpg")

# ... or fixed colour gains (red, blue) - this switches AWB off automatically
picam2.set_controls({"ColourGains": (1.6, 1.4)})
time.sleep(0.5)
picam2.capture_file("awb_manual.jpg")

# back to automatic white balance
picam2.set_controls({"AwbEnable": True})

# Image adjustments work inside the camera pipeline, not on the file afterwards
picam2.set_controls({"Contrast": 1.6, "Saturation": 1.6, "Sharpness": 1.0})
time.sleep(0.5)
picam2.capture_file("adjusted.jpg")

picam2.stop()

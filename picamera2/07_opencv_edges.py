#!/usr/bin/env python3
# Picamera2 example from the raspberry.tips tutorial
# https://raspberry.tips/raspberrypi-tutorials/picamera2-raspberry-pi-kamera-python
# Frames as NumPy arrays: Canny edge detection with OpenCV and the RGB/BGR pitfall.
import cv2
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration(main={"size": (1640, 1232)}))
picam2.start()

frame = picam2.capture_array("main")
print(frame.shape, frame.dtype)   # (1232, 1640, 3) uint8

# The array arrives in RGB order (libcamera calls the format "BGR888" - the name is inverted)
gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
edges = cv2.Canny(gray, 100, 200)
cv2.imwrite("edges.jpg", edges)

# OpenCV expects BGR when writing colour images - convert first, or red and blue swap
bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
cv2.imwrite("colour.jpg", bgr)
picam2.stop()

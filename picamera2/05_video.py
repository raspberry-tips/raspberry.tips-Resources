#!/usr/bin/env python3
# Picamera2 example from the raspberry.tips tutorial
# https://raspberry.tips/raspberrypi-tutorials/picamera2-raspberry-pi-kamera-python
# Record video: raw H.264 stream, MP4 via PyavOutput, and a fixed-length clip.
import time

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput, PyavOutput

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (1280, 720)}))

# 1) 5 seconds of raw H.264 - no container, VLC plays it, most other players do not
encoder = H264Encoder(bitrate=5_000_000)
picam2.start_recording(encoder, FileOutput("clip.h264"))
time.sleep(5)
picam2.stop_recording()

# 2) MP4 with correct timestamps: PyavOutput writes the container directly from Python.
#    FfmpegOutput pipes the stream to an external ffmpeg that re-timestamps every frame;
#    in our tests that produced files tagged as 60 fps with the wrong duration.
picam2.start_recording(H264Encoder(bitrate=5_000_000), PyavOutput("clip.mp4"))
time.sleep(5)
picam2.stop_recording()

# 3) Convenience call for a clip of fixed length
picam2.start_and_record_video("clip_10s.mp4", duration=10)

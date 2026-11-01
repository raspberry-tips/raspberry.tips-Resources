#!/bin/bash
# Install rpi-clone (Jeff Geerling's maintained fork) – supports NVMe and /boot/firmware.
# The original billw2/rpi-clone has not been maintained since 2020.
# Guide (DE): https://raspberry.tips/raspberrypi-tutorials/raspberry-pi-datensicherung-erstellen
# Guide (EN): https://raspberry.tips/en/raspberrypi-tutorials/raspberry-pi-backup-guide
set -e

curl -fsSL https://raw.githubusercontent.com/geerlingguy/rpi-clone/master/install | sudo bash

echo
echo "Usage:"
echo "  lsblk                  # find the target drive (e.g. sda for USB, mmcblk0 for the SD slot)"
echo "  sudo rpi-clone sda     # first clone (target is overwritten)"
echo "  sudo rpi-clone -f sda  # force fresh partitioning of a previously used target"
echo "  sudo rpi-clone -u sda  # later runs: sync changes only, no prompts"

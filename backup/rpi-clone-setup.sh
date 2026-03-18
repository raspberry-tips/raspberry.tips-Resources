#!/bin/bash
# rpi-clone Setup Script (geerlingguy Fork – Bookworm + Pi 5 kompatibel)
# Tutorial: https://raspberry.tips/raspberrypi-tutorials/raspberry-pi-datensicherung-erstellen
# WICHTIG: Nicht den originalen billw2/rpi-clone verwenden – der hat einen Bug unter Bookworm!

set -e

echo "Installiere rpi-clone (geerlingguy Fork)..."
sudo apt install git -y
git clone https://github.com/geerlingguy/rpi-clone.git /tmp/rpi-clone
cd /tmp/rpi-clone
sudo cp rpi-clone /usr/local/sbin/
rm -rf /tmp/rpi-clone

echo "rpi-clone erfolgreich installiert."
echo ""
echo "Verwendung:"
echo "  lsblk                    # Gerätename des Zielmediums herausfinden"
echo "  sudo rpi-clone sda       # Klon erstellen (sda = Zielmedium, anpassen!)"

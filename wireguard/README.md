# WireGuard VPN auf dem Raspberry Pi

Templates für einen WireGuard VPN-Server auf dem Raspberry Pi.

**Vollständiges Tutorial:** [raspberry.tips → WireGuard VPN Server einrichten](https://raspberry.tips/raspberrypi-tutorials/wireguard-vpn-server-auf-dem-raspberry-pi-einrichten)

## Dateien

- `wg0.conf` – Server-Konfiguration
- `client.conf` – Client-Konfiguration (Smartphone/PC)

## Schnellstart

```bash
sudo apt install wireguard wireguard-tools qrencode -y
cd /etc/wireguard && umask 077
wg genkey | tee server_private.key | wg pubkey > server_public.key
sudo cp wg0.conf /etc/wireguard/wg0.conf
# wg0.conf anpassen (Private Key, Client Public Keys eintragen)
sudo systemctl enable wg-quick@wg0 && sudo systemctl start wg-quick@wg0
```

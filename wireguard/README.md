# WireGuard VPN server on the Raspberry Pi

Config templates and commands for the raspberry.tips guide:

- English: https://raspberry.tips/en/raspberrypi-tutorials/wireguard-vpn-server-raspberry-pi
- Deutsch: https://raspberry.tips/raspberrypi-tutorials/wireguard-vpn-server-auf-dem-raspberry-pi-einrichten

The guide also explains when you don't need the Pi at all (routers with built-in WireGuard), how to check for CGNAT/DS-Lite, the router side (fixed IP, port forwarding of UDP 51820) and troubleshooting.

## Files

| File | Purpose |
|---|---|
| `wg0.conf` | Server config, goes to `/etc/wireguard/wg0.conf` on the Pi |
| `client.conf` | Client config for the phone, goes to `/etc/wireguard/clients/phone.conf` on the Pi |
| `client-laptop.conf` | Client config for a second device, goes to `/etc/wireguard/clients/laptop.conf` on the Pi |

Placeholders: `SERVER_PRIVATE_KEY`, `SERVER_PUBLIC_KEY`, `PHONE_PRIVATE_KEY`, `PHONE_PUBLIC_KEY`, `LAPTOP_PRIVATE_KEY`, `LAPTOP_PUBLIC_KEY`, `yourname` / `YOUR-TOKEN` (DuckDNS). `192.168.178.1` / `192.168.178.0/24` are FRITZ!Box defaults, replace them with your router's values.

All commands below are the ones from the guide, in the same order.

## 1. Dynamic DNS with DuckDNS

Option 1, in your router (custom dynamic DNS provider; username `none`, password = your token). Leave out DuckDNS's optional `&ipv6=<ip6addr>`, it would point IPv6 clients at the router instead of the Pi:

```
https://www.duckdns.org/update?domains=yourname&token=YOUR-TOKEN&ip=<ipaddr>
```

Option 3, script on the Pi (for routers without a custom provider). `duck.log` should say `OK`:

```bash
mkdir -p ~/duckdns
cd ~/duckdns
cat > duck.sh << 'EOF'
#!/bin/sh
echo url="https://www.duckdns.org/update?domains=yourname&token=YOUR-TOKEN&ip=" | curl -o ~/duckdns/duck.log -K -
EOF
chmod 700 duck.sh
./duck.sh
cat duck.log
```

Then run `crontab -e` and add this line at the bottom:

```
*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1
```

## 2a. Option A: PiVPN

PiVPN is only maintained on a best-effort basis. If you want UFW, turn it on before installing (see section 4), so PiVPN adds its own rules. Read the script before running it:

```bash
curl -sSfL https://install.pivpn.io -o pivpn-install.sh
less pivpn-install.sh
bash pivpn-install.sh
```

Devices: name the first one `phone`, the second one `laptop`. PiVPN also saves each config to `~/configs/<name>.conf` in the home directory of the user picked during installation.

```bash
pivpn add
pivpn -qr phone
pivpn add
pivpn -c
pivpn -r phone
```

## 2b. Option B: manual setup (current Raspberry Pi OS)

```bash
# Packages - iptables is not preinstalled, but the PostUp/PostDown rules need it
sudo apt update
sudo apt install wireguard qrencode iptables

# Keys - /etc/wireguard belongs to root, so open a root shell first ...
sudo -i
# ... then, inside the root shell:
cd /etc/wireguard
umask 077
wg genkey | tee server_private.key | wg pubkey > server_public.key
mkdir -p clients
wg genkey | tee clients/phone_private.key | wg pubkey > clients/phone_public.key
ls -l /etc/wireguard /etc/wireguard/clients
exit

# Interface name for the NAT rule (the name after "dev", e.g. eth0 or wlan0)
ip route get 1.1.1.1

# Server config: paste wg0.conf, fill in SERVER_PRIVATE_KEY and PHONE_PUBLIC_KEY
sudo cat /etc/wireguard/server_private.key
sudo cat /etc/wireguard/clients/phone_public.key
sudo nano /etc/wireguard/wg0.conf
sudo chmod 600 /etc/wireguard/wg0.conf

# IP forwarding that survives a reboot (/etc/sysctl.conf is no longer read)
echo "net.ipv4.ip_forward = 1" | sudo tee /etc/sysctl.d/99-wireguard.conf
sudo sysctl --system
sudo sysctl net.ipv4.ip_forward

# Start now and on every boot, then check for "listening port: 51820"
sudo systemctl enable --now wg-quick@wg0
sudo wg show

# Phone config: paste client.conf, fill in PHONE_PRIVATE_KEY, SERVER_PUBLIC_KEY, Endpoint
sudo cat /etc/wireguard/clients/phone_private.key
sudo cat /etc/wireguard/server_public.key
sudo nano /etc/wireguard/clients/phone.conf

# QR code for the WireGuard app (use -r, not "<", which fails with sudo)
sudo qrencode -t ansiutf8 -r /etc/wireguard/clients/phone.conf

# Optional, once scanned: remove the phone's private files from the Pi
sudo rm /etc/wireguard/clients/phone.conf /etc/wireguard/clients/phone_private.key
```

### Add more devices (laptop)

```bash
sudo -i
# inside the root shell:
cd /etc/wireguard
umask 077
wg genkey | tee clients/laptop_private.key | wg pubkey > clients/laptop_public.key
exit

# Add a [Peer] with LAPTOP_PUBLIC_KEY and AllowedIPs = 10.0.0.3/32 to wg0.conf
sudo cat /etc/wireguard/clients/laptop_public.key
sudo nano /etc/wireguard/wg0.conf

# Laptop config: paste client-laptop.conf, fill in LAPTOP_PRIVATE_KEY, SERVER_PUBLIC_KEY, Endpoint
sudo cat /etc/wireguard/clients/laptop_private.key
sudo cat /etc/wireguard/server_public.key
sudo nano /etc/wireguard/clients/laptop.conf

sudo systemctl restart wg-quick@wg0
```

The `[Peer]` section for `wg0.conf`:

```
[Peer]
# laptop
PublicKey = LAPTOP_PUBLIC_KEY
AllowedIPs = 10.0.0.3/32
```

## 3. Connect and test

Show a client file as text: `cat ~/configs/laptop.conf` (PiVPN) or `sudo cat /etc/wireguard/clients/laptop.conf` (manual). On Windows/macOS, save it as `laptop.conf` and use "Import tunnel(s) from file" in the WireGuard app. On a Linux laptop:

```bash
sudo apt install wireguard openresolv
sudo nano /etc/wireguard/wg0.conf
sudo chmod 600 /etc/wireguard/wg0.conf
sudo wg-quick up wg0
```

Test from outside (phone on mobile data, Wi-Fi off), then look for `latest handshake` on the Pi:

```bash
sudo wg show
```

## 4. Optional: UFW firewall

Allow SSH before enabling UFW. With PiVPN, these are the same rules PiVPN adds itself when UFW is already active during installation. Use `wlan0` instead of `eth0` if the Pi is on Wi-Fi.

```bash
sudo apt install ufw
sudo ufw allow 22/tcp
sudo ufw allow 51820/udp
sudo ufw route allow in on wg0 out on eth0
sudo ufw enable
```

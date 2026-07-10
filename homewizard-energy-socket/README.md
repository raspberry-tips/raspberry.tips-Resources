# HomeWizard Energy Socket – Verbrauchslogger

Begleit-Script zum Artikel **HomeWizard Energy Socket im Test – WLAN-Steckdose mit Home Assistant einbinden** auf [raspberry.tips](https://raspberry.tips).

`energy_logger.py` fragt die [lokale API v1](https://api-documentation.homewizard.com/docs/category/api-v1) der Energy Socket im Sekundentakt ab und schreibt Leistung (W) und Zählerstand (kWh) mit Zeitstempel in eine CSV-Datei – z. B. um den Anlaufstrom der Waschmaschine oder ein Lastprofil über den Tag aufzuzeichnen. Alles läuft komplett lokal, ganz ohne Cloud.

## Voraussetzungen

- HomeWizard Energy Socket im gleichen Netzwerk
- Lokale API in der HomeWizard-App aktiviert (Gerät öffnen → *Einstellungen der Steckdose* → *Lokale API*) – die App zeigt dort auch die IP-Adresse an
- Python 3 mit dem Paket `requests`:

```bash
sudo apt install python3-requests
```

## Verwendung

```bash
python3 energy_logger.py <IP-der-Energy-Socket> [ausgabe.csv]

# Beispiel:
python3 energy_logger.py 192.168.178.108 waschmaschine.csv
```

Beenden mit `Strg+C`. Die CSV-Datei hat drei Spalten:

```
timestamp,active_power_w,total_power_import_kwh
2026-07-10T14:42:58,0.0,0.011
```

## Energy Socket im Netzwerk finden

Alle HomeWizard-Geräte melden sich per mDNS:

```bash
sudo apt install avahi-utils
avahi-browse -rt _hwenergy._tcp
```

## Auswertung

Die CSV lässt sich direkt in LibreOffice/Excel öffnen oder mit ein paar Zeilen matplotlib plotten. Für Langzeit-Monitoring bietet sich InfluxDB + Grafana an – oder gleich die native [HomeWizard-Integration in Home Assistant](https://www.home-assistant.io/integrations/homewizard/), wie im Artikel beschrieben.

#!/usr/bin/env python3
"""Verbrauchslogger für die HomeWizard Energy Socket (lokale API v1).

Fragt die aktuelle Leistung im Sekundentakt ab und schreibt sie mit
Zeitstempel in eine CSV-Datei – z. B. um den Anlaufstrom der
Waschmaschine oder ein Lastprofil über den Tag aufzuzeichnen.

Verwendung:
    python3 energy_logger.py <IP-der-Energy-Socket> [ausgabe.csv]

Voraussetzung: Die lokale API muss in der HomeWizard-App aktiviert sein
(Gerät öffnen -> Einstellungen der Steckdose -> Lokale API).

Begleit-Script zum Artikel auf https://raspberry.tips
"""
import csv
import sys
import time
from datetime import datetime

import requests

DEFAULT_CSV = "energy_log.csv"
INTERVAL = 1  # Abfrage-Intervall in Sekunden


def main():
    if len(sys.argv) < 2:
        sys.exit(f"Verwendung: {sys.argv[0]} <IP-der-Energy-Socket> [ausgabe.csv]")
    ip = sys.argv[1]
    csv_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_CSV

    print(f"Logge {ip} -> {csv_path} (Strg+C zum Beenden)")
    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["timestamp", "active_power_w", "total_power_import_kwh"])
        try:
            while True:
                try:
                    data = requests.get(f"http://{ip}/api/v1/data", timeout=5).json()
                    writer.writerow([
                        datetime.now().isoformat(timespec="seconds"),
                        data["active_power_w"],
                        data["total_power_import_kwh"],
                    ])
                    f.flush()
                except requests.RequestException as e:
                    print(f"Fehler bei der Abfrage: {e}", file=sys.stderr)
                time.sleep(INTERVAL)
        except KeyboardInterrupt:
            print("\nLogging beendet.")


if __name__ == "__main__":
    main()

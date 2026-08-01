# Air-Quality-Dashboard mit Empfehlungsprofilen für Home Assistant

Begleitmaterial zum Artikel auf [raspberry.tips](https://raspberry.tips/smart-home/airthings-view-plus-test-home-assistant):
Luftqualitäts-Dashboard nach dem Vorbild der Airthings-App — Ampel-Anzeigen mit den
offiziellen Airthings-Schwellwerten plus Empfehlungsprofile (Kopfschmerzen, Schlaf,
Produktivität, Allergie) als Template-Sensoren. Funktioniert mit jedem
Luftqualitäts-Sensor, es müssen nur die Entity-IDs angepasst werden.

## Dateien

| Datei | Zweck |
|---|---|
| `packages/airthings_luftprofile.yaml` | Profil-Sensoren + Luftdruck-Trend (als HA-Package) |
| `dashboard_luftqualitaet.yaml` | Dashboard nur mit Bordmitteln (keine HACS-Karten nötig) |
| `dashboard_luftqualitaet_styled.yaml` | Hübschere Variante mit Mushroom, mini-graph-card und Gauge Card Pro (HACS) |

## Kurzanleitung

1. Package-Support in der `configuration.yaml` aktivieren:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```
2. `packages/airthings_luftprofile.yaml` nach `config/packages/` kopieren und die
   Entity-IDs anpassen (Entwicklerwerkzeuge → Zustände).
3. Konfiguration prüfen → Home Assistant neu starten.
4. Neues Dashboard anlegen → Roh-Konfigurationseditor → Inhalt einer der beiden
   Dashboard-Dateien einfügen (Entity-IDs ebenfalls anpassen).

**Achtung Umlaute:** Home Assistant kürzt Umlaute in Entity-IDs zu a/o/u —
aus „Luftprofil Produktivität" wird `sensor.luftprofil_produktivitat`.

Die komplette Schritt-für-Schritt-Anleitung mit Screenshots gibt es im Artikel.

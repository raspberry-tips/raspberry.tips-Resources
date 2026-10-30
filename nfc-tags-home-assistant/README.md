# NFC-Tags in Home Assistant: Erinnern, bis es erledigt ist

Script und Konfiguration zum Artikel [NFC-Tags in Home Assistant: Der Cent-Trick gegen Vergessen](https://raspberry.tips/smart-home/nfc-tags-in-home-assistant-erinnerung) auf raspberry.tips (English: [Home Assistant NFC Tags: Reminders That Stop When It's Done](https://raspberry.tips/en/smart-home/home-assistant-nfc-tags-reminders)). Die englische Fassung nutzt die Kennungen `dishwasher`/`pill` und englische Helfernamen, die Dateien hier entsprechen der deutschen. Ein NFC-Sticker an Spülmaschine oder Tablettenbox beendet eine Erinnerung von Home Assistant erst, wenn er mit dem Handy gescannt wird.

## Dateien

| Datei | Beschreibung |
|---|---|
| `nfc_ha_tag.py` | Schreibt `https://www.home-assistant.io/tag/<kennung>` mit einem PN532 auf einen NTAG213-Sticker, liest gegen und sperrt ihn auf Wunsch (`--lock`) |
| `automation_spuelmaschine_ausraeumen.yaml` | Erinnert alle 30 Minuten (7–22 Uhr), bis der Sticker `spuelmaschine` gescannt wird |
| `automation_tablette_genommen.yaml` | Öffnet die Tablette um 3 Uhr, erinnert ab 8 Uhr; ein zweiter Scan meldet, wann sie genommen wurde |
| `dashboard_kacheln_spuelmaschine.yaml` | Kacheln „offen“ / „ausgeräumt“ für die Übersicht |
| `dashboard_kacheln_tablette.yaml` | Kacheln „offen“ / „zuletzt genommen“ |

## Sticker beschreiben (PN532 am Raspberry Pi)

PN532 per I²C anschließen und die Bibliothek installieren wie in [PN532 am Raspberry Pi 5](https://raspberry.tips/raspberrypi-tutorials/pn532-am-raspberry-pi-5) beschrieben (virtuelle Umgebung `~/nfc-env`). Dann:

```bash
git clone https://github.com/raspberry-tips/raspberry.tips-Resources.git
cd raspberry.tips-Resources/nfc-tags-home-assistant
source ~/nfc-env/bin/activate
python nfc_ha_tag.py spuelmaschine
```

Sticker flach und mittig auf die Antenne legen. Während des Schreibens nicht mit Strg+C abbrechen.

### Sperren

```bash
python nfc_ha_tag.py spuelmaschine --lock
```

**Endgültig:** Ein gesperrter Sticker lässt sich nie wieder beschreiben, Lesen und Scannen funktionieren weiter. Das Script fragt vorher nach (`LOCK` eintippen), schreibt und prüft die Adresse, setzt erst dann die Lock-Bits (NTAG213-Datenblatt, Abschnitte 8.5.2–8.5.4) und liest sie zur Kontrolle zurück. Nur für NTAG213.

## Automationen

Helfer anlegen (Einstellungen → Geräte & Dienste → Helfer):

- Umschalter „Spülmaschine ausräumen“ → `input_boolean.spulmaschine_ausraumen`
- Umschalter „Tablette nehmen“ → `input_boolean.tablette_nehmen`
- Datum- und Uhrzeit-Eingabe „Tablette zuletzt genommen“ → `input_datetime.tablette_zuletzt_genommen`

YAML in eine neue Automation einfügen (Drei-Punkte-Menü → In YAML bearbeiten) und anpassen:

- `notify.mobile_app_euer_iphone` durch den Benachrichtigungsdienst eures Handys ersetzen (jedes Vorkommen)
- `tag_id` auf die Kennung eures Stickers setzen
- `url: /dashboard-erinnerungen/0` passt zu einem Dashboard mit der Adresse `dashboard-erinnerungen`

Die Spülmaschinen-Automation erwartet, dass eure Fertigmeldung den Helfer einschaltet, z. B. die aus [Spülmaschine oder Waschmaschine fertig?](https://raspberry.tips/smart-home/spuelmaschine-waschmaschine-fertig-benachrichtigung-home-assistant).

Getestet im Oktober 2026 mit Home Assistant 2026.10, der iPhone-App und einem Raspberry Pi 5 (Raspberry Pi OS): Beide Automationen laufen so in Home Assistant, im Test mit eigenem Benachrichtigungsdienst und eigener Dashboard-Adresse.

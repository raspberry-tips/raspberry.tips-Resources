# Home Assistant NFC tags: reminders that stop when it's done

Script and configuration for the article [Home Assistant NFC Tags: Reminders That Stop When It's Done](https://raspberry.tips/en/smart-home/home-assistant-nfc-tags-reminders) on raspberry.tips. An NFC sticker on the dishwasher or the pill organiser ends a Home Assistant reminder only when you scan it with your phone. The German version of these files is in the parent folder.

## Files

| File | Description |
|---|---|
| `nfc_ha_tag.py` | Writes `https://www.home-assistant.io/tag/<tag-id>` to an NTAG213 sticker with a PN532, reads it back and locks it on request (`--lock`) |
| `automation_dishwasher_unload.yaml` | Reminds every 30 minutes (7 am to 10 pm) until the `dishwasher` sticker is scanned |
| `automation_medication_taken.yaml` | Makes the medication due at 3 am and reminds from 8 am; a second scan shows when it was taken |
| `dashboard_tiles_dishwasher.yaml` | "Needs unloading" / "Unloaded" tiles for the Reminders dashboard |
| `dashboard_tiles_medication.yaml` | "Still due" / "Last taken" tiles |

## Writing stickers (PN532 on a Raspberry Pi)

Connect the PN532 over I²C and install the library as described in [PN532 on the Raspberry Pi 5](https://raspberry.tips/en/raspberrypi-tutorials/pn532-on-the-raspberry-pi-5) (virtual environment `~/nfc-env`). Then:

```bash
git clone https://github.com/raspberry-tips/raspberry.tips-Resources.git
cd raspberry.tips-Resources/nfc-tags-home-assistant/en
source ~/nfc-env/bin/activate
python nfc_ha_tag.py dishwasher
```

Place the sticker flat in the middle of the antenna. Don't stop the script with Ctrl+C while it's writing.

### Locking

```bash
python nfc_ha_tag.py frontdoor --lock
```

**Permanent:** a locked sticker can never be rewritten; reading and scanning still work. The script asks first (type `LOCK`), writes and checks the URL, only then sets the lock bits (NTAG213 datasheet, sections 8.5.2 to 8.5.4) and reads them back. NTAG213 only.

## Automations

Create the helpers (Settings → Devices & services → Helpers):

- Toggle "Dishwasher unload" → `input_boolean.dishwasher_unload`
- Toggle "Take pill" → `input_boolean.take_pill`
- Date and/or time helper "Pill last taken" (date and time) → `input_datetime.pill_last_taken`

Paste the YAML into a new automation (three-dot menu → Edit in YAML) and adjust:

- replace every `notify.mobile_app_your_iphone` with your phone's notification service
- set `tag_id` to your sticker's tag ID
- `url: /dashboard-reminders/0` matches a dashboard with the URL `dashboard-reminders`; without the dashboard, delete the `url` line

The dishwasher automation expects your done notification to switch the helper on, for example the one from [Dishwasher or washing machine done notification](https://raspberry.tips/en/smart-home/dishwasher-washing-machine-done-notification-home-assistant).

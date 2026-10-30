import signal
import sys

import board
import busio
from adafruit_pn532.i2c import PN532_I2C

# usage: python nfc_ha_tag.py <tag-id> [--lock]
args = [a for a in sys.argv[1:] if a != "--lock"]
LOCK = "--lock" in sys.argv[1:]
# Home Assistant tag URL; the part after /tag/ becomes the tag ID in Home Assistant
TAG_ID = args[0] if args else "spuelmaschine"
URL = f"www.home-assistant.io/tag/{TAG_ID}"

running = True


def stop(signum, frame):
    # finish the current command first, so the PN532 is not left mid-command
    global running
    running = False


signal.signal(signal.SIGINT, stop)


def ndef_url_message(url):
    # NDEF URI record, prefix 0x04 = "https://"
    payload = bytes([0x04]) + url.encode()
    record = bytes([0xD1, 0x01, len(payload), 0x55]) + payload
    # TLV: 0x03 = NDEF message, then length, record, 0xFE = terminator
    data = bytes([0x03, len(record)]) + record + bytes([0xFE])
    # pad to full 4-byte pages
    return data + bytes((-len(data)) % 4)


def write_page(page, block):
    # a weak field can drop single writes; select the sticker again and retry
    for _ in range(3):
        if pn532.ntag2xx_write_block(page, block):
            return True
        pn532.read_passive_target(timeout=0.5)
    return False


def lock_ntag213():
    # NTAG213 datasheet 8.5.2-8.5.4: all lock bits are OR'ed in and can never be cleared
    # dynamic lock bytes (page 0x28): pages 16-39 read-only, RFUI bits stay 0
    if not write_page(0x28, bytes([0xFF, 0x0F, 0x3F, 0x00])):
        return False
    # capability container byte 3 = 0x0F: NFC Forum "read-only" flag for phones
    if not write_page(3, bytes([0x00, 0x00, 0x00, 0x0F])):
        return False
    # static lock bytes (page 2, bytes 2-3): pages 3-15 read-only; bytes 0-1 are ignored
    return write_page(2, bytes([0x00, 0x00, 0xFF, 0xFF]))


def lock_verified():
    # the PN532 reports some refused writes as OK, so read the lock bits back
    static = pn532.ntag2xx_read_block(2)
    cc = pn532.ntag2xx_read_block(3)
    dynamic = pn532.ntag2xx_read_block(0x28)
    if None in (static, cc, dynamic):
        return False
    return static[2:4] == b"\xff\xff" and cc[3] == 0x0F and dynamic[0:3] == b"\xff\x0f\x3f"


if LOCK:
    print("--lock makes the sticker read-only FOREVER. It can never be rewritten.")
    if input("Type LOCK to continue: ").strip() != "LOCK":
        sys.exit("Not locking. Nothing was written.")

i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)
pn532.SAM_configuration()

data = ndef_url_message(URL)
print(f"Writing https://{URL} ({len(data)} bytes, {len(data) // 4} pages)")
print("Hold the sticker on the reader ... (stop with Ctrl+C)")

uid = None
while running and uid is None:
    uid = pn532.read_passive_target(timeout=0.5)
if uid is None:
    sys.exit("Stopped.")
print(f"Sticker found, UID {uid.hex(':')}")

# page 3 = capability container; E1 = NDEF formatted, 0x12 = 144 bytes (NTAG213)
cc = pn532.ntag2xx_read_block(3)
print(f"Capability container: {cc.hex(' ')}")
if cc[0] != 0xE1:
    sys.exit("Not NDEF formatted - is this an NTAG sticker?")
if cc[3] != 0x00:
    sys.exit("Sticker is read-only (locked) and cannot be rewritten.")
if len(data) > cc[2] * 8:
    sys.exit("URL too long for this sticker.")
if LOCK and cc[2] != 0x12:
    sys.exit("--lock only supports NTAG213 stickers. Nothing was written.")


# user memory starts at page 4
for i in range(0, len(data), 4):
    if not write_page(4 + i // 4, data[i:i + 4]):
        sys.exit(f"Writing page {4 + i // 4} failed - keep the sticker still and retry.")

check = b"".join(pn532.ntag2xx_read_block(4 + i // 4) for i in range(0, len(data), 4))
if check != data:
    sys.exit("Read-back differs - write again.")
print(f"Done. Verified: https://{URL}")

if LOCK:
    if lock_ntag213() and lock_verified():
        print(f"Locked. Capability container now: {pn532.ntag2xx_read_block(3).hex(' ')}")
    else:
        sys.exit("Locking failed or incomplete - lock bits could not be verified.")

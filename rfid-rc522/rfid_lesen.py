from mfrc522_pi5 import MFRC522
import time

reader = MFRC522()

print("Halte eine RFID-Karte oder einen Schluesselanhaenger an den Leser...")
print("(Abbrechen mit Strg+C)\n")

try:
    while True:
        (status, TagType) = reader.MFRC522_Request(MFRC522.PICC_REQIDL)
        if status == MFRC522.MI_OK:
            (status, uid) = reader.MFRC522_Anticoll()
            if status == MFRC522.MI_OK:
                uid_str = "-".join([str(x) for x in uid[:4]])
                print(f"Tag erkannt! UID: {uid_str}")
        time.sleep(0.1)
except KeyboardInterrupt:
    reader.cleanup()
    print("\nProgramm beendet.")

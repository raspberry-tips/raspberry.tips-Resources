from mfrc522_pi5 import MFRC522
import time

reader = MFRC522()

print("Hold an RFID card or key fob up to the reader...")
print("(Press Ctrl+C to quit)\n")

try:
    while True:
        (status, TagType) = reader.MFRC522_Request(MFRC522.PICC_REQIDL)

        if status == MFRC522.MI_OK:
            (status, uid) = reader.MFRC522_Anticoll()

            if status == MFRC522.MI_OK:
                uid_str = "-".join([str(x) for x in uid[:4]])
                print(f"Tag detected! UID: {uid_str}")

        time.sleep(0.1)

except KeyboardInterrupt:
    reader.cleanup()
    print("\nProgram stopped.")

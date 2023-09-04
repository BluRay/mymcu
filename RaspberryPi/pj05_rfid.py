# (For Pi)https://pypi.org/project/mfrc522/  [A library to integrate the MFRC522 RFID readers with the Raspberry Pi]
# (For Pico)https://github.com/kevinmcaleer/pico-rfid
from time import sleep
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        print("ID: %s\nText: %s" % (id,text))
        sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise

# TODO RFID-RC522  https://gitee.com/ajianlee/RC522
# https://blog.csdn.net/m0_64596200/article/details/129764722
# http://docs.tpyboard.com/zh/latest/tpyboard/driver/mfrc522/
# (For Pi)https://pypi.org/project/mfrc522/
# (For Pico)https://github.com/kevinmcaleer/pico-rfid
from mfrc522 import MFRC522
import utime

# RFID Signal	  Pico Pin
# SCK	          GP2
# MOSI	        GP3
# MISO	        GP4
# RST	          GP0
# SDA	          GP1
              
reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)

print("")
print("Place card into reader")
print("")

PreviousCard = [0]

try:
    while True:
        reader.init()
        (stat, tag_type) = reader.request(reader.REQIDL)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if uid == PreviousCard:
                continue

            if stat == reader.OK:
                print("Card detected {}  uid={}".format(hex(int.from_bytes(bytes(uid),"little",False)).upper(),reader.tohexstring(uid)))
                firstSectorKey = [0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5]
                nextSectorKey = [0xD3, 0xF7, 0xD3, 0xF7, 0xD3, 0xF7]
                #defaultKey = [255,255,255,255,255,255]

                #read MAD sector  (first sector)
                if reader.MFRC522_DumpClassic1K(uid, Start=0, End=4, keyA=firstSectorKey)== reader.OK:
                    #read the rest of the card
                    reader.MFRC522_DumpClassic1K(uid, Start=4, End=64, keyA=nextSectorKey)
                print("Done")
                PreviousCard = uid
        else:
            PreviousCard=[0]
        utime.sleep_ms(50)                

except KeyboardInterrupt:
    print("Bye")

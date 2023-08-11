from ST7735 import TFT,TFTColor
from machine import SPI,Pin
import time
spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=None)
'''
https://blog.csdn.net/weixin_45616112/article/details/122029723
GND   GND
VDD   VBUS
SCL   GP10
SDA   GP11
RST   GP17
DC    GP16
CS    GP18
'''
tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

def showPic(file):
    f=open(file, 'rb')
    if f.read(2) == b'BM':  #header
        dummy = f.read(8) #file size(4), creator bytes(4)
        offset = int.from_bytes(f.read(4), 'little')
        hdrsize = int.from_bytes(f.read(4), 'little')
        width = int.from_bytes(f.read(4), 'little')
        height = int.from_bytes(f.read(4), 'little')
        if int.from_bytes(f.read(2), 'little') == 1: #planes must be 1
            depth = int.from_bytes(f.read(2), 'little')
            if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:#compress method == uncompressed
                print("Image size:", width, "x", height)
                rowsize = (width * 3 + 3) & ~3
                if height < 0:
                    height = -height
                    flip = False
                else:
                    flip = True
                w, h = width, height
                if w > 128: w = 128
                if h > 160: h = 160
                tft._setwindowloc((0,0),(w - 1,h - 1))
                for row in range(h):
                    if flip:
                        pos = offset + (height - 1 - row) * rowsize
                    else:
                        pos = offset + row * rowsize
                    if f.tell() != pos:
                        dummy = f.seek(pos)
                    for col in range(w):
                        bgr = f.read(3)
                        tft._pushcolor(TFTColor(bgr[2],bgr[1],bgr[0]))
    f.close()
    spi.deinit()

while True:
    showPic('yinan128_160.bmp')
    time.sleep(5)
    showPic('yinan128_160b.bmp')
    time.sleep(5)
    showPic('pei128_160.bmp')
    time.sleep(5)
    showPic('yinan128_160c.bmp')
    time.sleep(5)

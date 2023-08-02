from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from PIL import ImageFont
from time import sleep
from datetime import datetime
 
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)
fontCN = ImageFont.truetype("msyh.ttc", 32)
fontEN = ImageFont.truetype("arial.ttf", 24)
device.capabilities(128,64,0,'1')
while True: # 程序结束后屏幕将熄灭
  currentDateAndTime = datetime.now()
  currentTime = currentDateAndTime.strftime("%H:%M:%S")
  with canvas(device) as draw:
    #print(device.bounding_box) # (0, 0, 127, 63)
    draw.rectangle((0, 1, 127, 63), outline="white", fill="black") # 让屏幕周围显示一个框
    draw.text((0, 0), "Hi杨一楠", font=fontCN, fill="white")
    #draw.text((0, 35), "GoodBoy", font=fontEN, fill="white")
    draw.text((0, 35), currentTime, font=fontEN, fill="white")
    #device.show()
  sleep(5)

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from PIL import ImageFont
from time import sleep
 
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)
font = ImageFont.truetype("arial.ttf", 16)
#while True: # 程序结束后屏幕将熄灭
device.capabilities(128,32,0,'1')
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black") # 让屏幕周围显示一个框
    draw.text((5, 5), "Hello World", font=font, fill="white")
    #device.show()
sleep(15)

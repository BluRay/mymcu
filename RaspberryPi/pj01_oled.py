from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from time import sleep
 
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)
#while True:
device.capabilities(128,32,0,'1')
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black") # 让屏幕周围显示一个框
    draw.text((5, 5), "Hello World", fill="white", font_size=16)
    #device.show()
sleep(15)

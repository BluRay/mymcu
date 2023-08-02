# 开启新线程用于OLED屏显示，字符过长时自动增加滚动效果
import _thread
# from luma.core.interface.serial import i2c, spi
# from luma.core.render import canvas
# from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
# from PIL import ImageFont
from time import sleep
from datetime import datetime
import time
# serial = i2c(port=1, address=0x3C)
# device = ssd1306(serial)

#global msg
def work():
  global global_msg
  global_msg = ""
  count = 0
  while count < 5:
    count += 1
    global_msg = "work:{}".format(count)
    print("msg:" + global_msg)
    sleep(5)

def oled_display(text):
  global global_msg
  global_msg = ""
  count = 0
  while count < 50:
    count += 1
    print("%s: %s" % (time.ctime(time.time()), text + global_msg ))
    sleep(2)
print("start_new_thread start")
try:
  _thread.start_new_thread(oled_display, ("msg:",))
except:
  print ("Error")
print("start_new_thread end")
work()
while 1:
  pass
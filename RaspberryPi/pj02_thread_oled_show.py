# 开启新线程用于OLED屏显示，字符过长时自动增加滚动效果
import _thread
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from PIL import ImageFont
from time import sleep
from datetime import datetime
import time

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)
fontCN = ImageFont.truetype("msyh.ttc", 36)
fontEN = ImageFont.truetype("arial.ttf", 24)
device.capabilities(128,64,0,'1')

def work():
  global global_msg
  global_msg = ""
  sleep(5)
  global_msg = "送别"
  sleep(3)
  global_msg = "长亭外 古道边"
  sleep(5)
  global_msg = "芳草碧连天"
  sleep(5)
  global_msg = "晚风拂柳笛声残"
  sleep(8)
  global_msg = "夕阳山外山"
  sleep(5)
  global_msg = "天之涯 地之角"
  sleep(8)
  global_msg = "知交半零落"
  sleep(5)
  global_msg = "一壶浊酒尽余欢"
  sleep(8)
  global_msg = "今宵别梦寒"
  sleep(5)
  '''
  count = 0
  while count < 5:
    count += 1
    global_msg = "work:{}".format(count)
    print("msg:" + global_msg)
    sleep(5)
  '''

def oled_display(text):
  global global_msg
  global_msg = ".Loading."
  msg = ""
  count = 0
  while count < 50:
    count += 1
    if (msg != global_msg):
      count = 0
    msg = global_msg
    #print("%s: %s" % (time.ctime(time.time()), text + global_msg ))
    with canvas(device) as draw:
      draw.text((0 - count*6, 0), msg, font=fontCN, fill="white")
    #sleep(0.005)
    if count == 50:
    	count = 0
print("start_new_thread start")
try:
  _thread.start_new_thread(oled_display, ("msg:",))
except:
  print ("Error")
print("start_new_thread end")
work()
work()
global_msg = "...no msg..."
while 1:
  pass
# https://doc.itprojects.cn/0006.zhishi.esp32/02.doc/index.html#/02.led
from machine import Pin
from time import sleep

pin2 = Pin(15, Pin.OUT)
while(1):
  pin2.value(1)
  sleep(1)
  pin2.value(0)
  sleep(1)
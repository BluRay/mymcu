# 红黄绿灯 闪烁
from machine import Pin # 从 machine 中加载 Pin
from time import sleep # 从 time 中加载 sleep

led_red = Pin(16, Pin.OUT)  # 定义引脚编号GP16，引脚模式为输出 红色
led_yel = Pin(17, Pin.OUT)  # 定义引脚编号GP17，引脚模式为输出 黄色
led_gre = Pin(18, Pin.OUT)  # 定义引脚编号GP18，引脚模式为输出 黄色

def rygloop():
    led_red.value(1)
    led_yel.value(0)
    led_gre.value(0)
    sleep(1)
    led_red.value(0)
    led_yel.value(1)
    led_gre.value(0)
    sleep(1)
    led_red.value(0)
    led_yel.value(0)
    led_gre.value(1)
    sleep(1)
def rygblink():
    led_red.value(1)
    led_yel.value(1)
    led_gre.value(1)
    sleep(0.2)
    led_red.value(0)
    led_yel.value(0)
    led_gre.value(0)
    sleep(0.2)
while(1):  # 永远循环
    #led_red.toggle() # 触发led，如果led是高电平（亮），那么就变成低电平（熄灭），反之亦然。
    #led_yel.toggle()
    #led_gre.toggle()
    for i in range(5):
        rygblink()
    for i in range(12):
        rygloop()

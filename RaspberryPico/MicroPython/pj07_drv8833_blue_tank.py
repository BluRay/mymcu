# 蓝牙控制 drv8833 操作电机 驱动履带车
import utime
import uos
from machine import Pin

# 创建两组对象，motor1a和motor1b。这些将存储用作输出的GPIO引脚号，以控制DRV8833电机控制器。
motor1a = Pin(14, Pin.OUT)
motor1b = Pin(15, Pin.OUT)
motor2a = Pin(17, Pin.OUT)
motor2b = Pin(16, Pin.OUT)

print(uos.uname())      #列出開發板的資訊
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(16), rx=machine.Pin(17))
print(uart)

led = machine.Pin(25, machine.Pin.OUT)	# 处理蓝牙命令时亮灯
led.value(0)
rxData = bytes()
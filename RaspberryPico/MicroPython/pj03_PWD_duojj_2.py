# Raspberry Pi Pico 超声波 电位器 控制舵机
'''
伺服电机红线连接到 Pico Vbus 引脚（5V）
伺服电机棕色线连接到 Pico GND
伺服电机黄线连接到 Pico PWM 引脚（GP16）
电位器 GND 连接到 Pico GND
电位器 VCC 连接到 Pico 3.3V
电位器中间引脚连接到 Pico ADC 引脚（GP28）
'''

from machine import Pin, PWM, ADC #import libraries for Pin, PWM, ADC
import time

# HC-SR04# 超声波测距仪
trig = machine.Pin(15,machine.Pin.OUT)
echo = machine.Pin(14,machine.Pin.IN)

# 超声波 距离计算
def distance():
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    while echo.value() == 0:
        pass
    while echo.value() == 1:
        ts = time.ticks_us()
        while echo.value() == 1:
            pass
        te = time.ticks_us()
        tc = te - ts
        distance = round((tc*170)/10000, 2)
    return distance
#adc = ADC(Pin(28)) #set Potentiometer analog input from GP28 pin

servoPin = PWM(Pin(16)) #set servo pwm output to GP16 pin
servoPin.freq(50) #set servo frequency 50
'''
servoPin.duty_u16(4915)  # 4915是90度
sleep(2)
servoPin.duty_u16(8192)  # 8192是180度
sleep(2)
servoPin.duty_u16(1638)  # 1638是0度
sleep(2)
'''
def servo(degrees): #rotate servo arm to degrees position
  # limit degrees beteen 0 and 180
  if degrees > 180: degrees=180
  if degrees < 0: degrees=0
  # set max and min duty
  maxDuty=8192
  minDuty=1638
  # new duty is between min and max duty in proportion to its value
  newDuty=minDuty+(maxDuty-minDuty)*(degrees/180)
  print(int(newDuty))
  # newDuty = 1638
  # servo PWM value is set
  servoPin.duty_u16(int(newDuty))

while True:
  # 读取ADC电位器数值
  #value=adc.read_u16() #read Potentiometer value
  #print(value)
  #degree=value*180/65500 #convert Potentiometer value to a servo position angle
  '''
  value = 0  # 角度 取ADC电位数值时需换算成角度
  servo(value) #rotate servo to that angle
  sleep(0.3)
  '''
  
  dist = distance()
  print('distance:', dist, 'cm')
  if dist < 10:
    servo(135)
  if dist >= 10:
    servo(0)
  time.sleep(0.8)

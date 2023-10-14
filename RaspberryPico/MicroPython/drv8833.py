# 用树莓派Pico 控制电机 https://www.eet-china.com/mp/a38406.html
# 
# 管脚说明：
# ANI1：AO1的逻辑输入控制端口，电平0-5V。
# AIN2：AO2的逻辑输入控制端口，电平0-5V。
# BNI1：BO1的逻辑输入控制端口，电平0-5V。
# BIN2：BO2的逻辑输入控制端口，电平0-5V。
# AO1、AO2为1路H桥输出端口，接一个直流电机的两个脚。
# BO1、BO2为2路H桥输出端口，接另一个外直接电机的两个脚。
# GND：接地。
# VM：芯片和电机供电脚，电压范围2.7 V – 10.8 V。
# STBY：接地或悬空芯片不工作，无输出，接5V工作；电平0-5V。
# NC：空脚

import utime
from machine import Pin

# 创建两个对象，motor1a和motor1b。这些将存储用作输出的GPIO引脚号，以控制DRV8833电机控制器。
motor1a = Pin(14, Pin.OUT)
motor1b = Pin(15, Pin.OUT)

# 创建一个使电动机“前进”的函数。为此，我们需要将一个引脚拉高，另一个引脚拉低。这继而将我们的预期方向传达给电机控制器，并且相应的输出引脚将紧随其后，迫使电机沿设定方向移动。
def forward():
	motor1a.high()
  motor1b.low()
  
# 创建一个向后移动的函数。这会看到GPIO引脚状态反转，从而导致电动机沿相反方向旋转。
def backward():
  motor1a.low()
  motor1b.high()
  
# 创建一个停止电动机的函数。通过将两个引脚都拉低，我们告诉电动机控制器停止电动机的所有运动。
def stop():
  motor1a.low()
  motor1b.low()

while True:
	# TODO
	forward()
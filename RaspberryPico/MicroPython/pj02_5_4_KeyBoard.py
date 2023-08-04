# RaspberryPico 5*4键盘输入
from machine import Pin,Timer,I2C
import utime

led_red = Pin(17, Pin.OUT)  # 定义引脚编号GP16，引脚模式为输出 红色
led_yel = Pin(15, Pin.OUT)  # 定义引脚编号GP17，引脚模式为输出 黄色
led_gre = Pin(14, Pin.OUT)  # 定义引脚编号GP18，引脚模式为输出 黄色

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
keyName = [['7','8','9','E'],
           ['4','5','6','D'],
           ['1','2','3','U'],
           ['A','B','#','*'],
           ['L','0','R','N']]
keypadRowPins = [12,16,20,21,22]
keypadColPins = [6,13,19,26]
row = []
col = []
keypadState = [];
for i in keypadRowPins:
    row.append(Pin(i,Pin.IN,Pin.PULL_UP))
    keypadState.append([0,0,0,0])
for i in keypadColPins:
    col.append(Pin(i,Pin.OUT))

def keypadRead():
    global row
    j_ifPressed = -1
    i_ifPressed = -1
    for i in range(0,len(col)):
        col[i].low()
        utime.sleep(0.005) #settling time
        for j in range(0,len(row)):
            pressed = not row[j].value()
            if(pressed and (keypadState[j][i] != pressed)): #state changed to high
                keypadState[j][i] = pressed
            elif(not pressed and (keypadState[j][i] != pressed)): # state changed to low
                keypadState[j][i] = pressed
                j_ifPressed = j
                i_ifPressed = i
        col[i].high()
    if(j_ifPressed != -1 and i_ifPressed != -1):
        return keyName[j_ifPressed][i_ifPressed]
    else:
        return -1
if __name__ == '__main__':
    while True:
        key = keypadRead()
        if(key != -1):
            print(key)
        if(key == 'A'):
            led_red.toggle()

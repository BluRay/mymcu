# -*- coding: utf-8 -*-
# I2C AHT10 温度湿度传感器
#!/usr/bin/python3
# https://github.com/Thinary/AHT10/blob/master/src/Thinary_AHT10.cpp
# https://myhydropi.com/raspberry-pi-i2c-temperature-sensor
# cleaned up and documented smbus 1 and some errors
# GJ 03-2020
# i2cdetect -y 0
# smbus是Python的一个扩展库，它提供了对I2C总线的访问和操作 安装：pip3 install smbus
from smbus2 import SMBus
import time

# Get I2C bus
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = SMBus(3) # 由26pin的原理图可知，可用的i2c为i2c3
# when you have a 121 IO Error, uncomment the next pause
# time.sleep(1) #wait here to avoid 121 IO Error

def getAht10Data():
    config = [0x08, 0x00]
    bus.write_i2c_block_data(0x38, 0xE1, config)
    time.sleep(0.5)
    byt = bus.read_byte(0x38)
    MeasureCmd = [0x33, 0x00]
    bus.write_i2c_block_data(0x38, 0xAC, MeasureCmd)
    time.sleep(0.5)
    data = bus.read_i2c_block_data(0x38,0x00,6)
    temp = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
    ctemp = ((temp*200) / 1048576) - 50
    tmp = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
    ctmp = int(tmp * 100 / 1048576)
    return [ctemp, ctmp]

def fileAddLine(str):
  # r+	打开一个文件用于读写。文件指针将会放在文件的开头。
  # a   打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
  # a+	打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
  with open('temphumi.txt', "a", encoding="utf-8") as file_obj:
    #file_obj.read()
    file_obj.write('\n' + str)

# 当前温度湿度写到文件
data = getAht10Data()
fileAddLine(time.strftime('%Y-%m-%d %H:%M', time.localtime()) + ' ' + str(round(data[0], 2)) + '|' + str(round(data[1], 2)))

'''
# 显示当前温度湿度
while(1):
    data = getAht10Data()
    # print(u'Temperature: {0:.2f}°C Humidity: {0:.2f}%'.format(data[0], data[1]))
    print ('温度: %s°C 湿度: %s%% \t\t  \r' % (round(data[0], 2), round(data[1], 2)),end = "")	
    time.sleep(2)
'''
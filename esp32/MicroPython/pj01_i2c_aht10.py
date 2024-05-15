# I2C 连接 AHT10 温湿度传感器
# ESP32默认的I2C引脚为：
# GPIO 21 （SDA）
# GPIO 22 （SCL）
# 其实在ESP32中任何引脚都可以定义为SDA或SCL，但不推荐这么做。
import utime
from machine import Pin, I2C

import ahtx0

# I2C for the Wemos D1 Mini with ESP8266
i2c = I2C(scl=Pin(5), sda=Pin(4))

# Create the sensor object using I2C
sensor = ahtx0.AHT10(i2c)

while True:
    print("\nTemperature: %0.2f C" % sensor.temperature)
    print("Humidity: %0.2f %%" % sensor.relative_humidity)
    utime.sleep(5)
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

# TODO 连接默认WIFI配置 连接不上时开启AP 通过手机连接热点 配置WIFI信息
# TODO 可配置多个WIFI 自动连接信号最强的WIFI 没有连接WIFI时保持N条数据在文件中
# TODO 连接tm1637 4位数码管 显示实时温湿度
# TODO 控制继电器
# TODO 采集GPS数据并上传

import time
import ahtx0
from machine import Pin, SoftI2C, Timer
from ssd1306 import SSD1306_I2C
import urequests as requests

wifi_ssd = 'MiWiFi'     # WIFI名称
wifi_psd = '07422770'   # WIFI密码

remote_config_url = 'http://120.24.188.63:8080/config'  # 获取配置地址
remote_postdb_url = 'http://120.24.188.63:8080/post'    # 接收数据地址

temperature = '0'       # 温度
humidity = '0'          # 湿度

# 连接无线网络
def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('MiWiFi', '07422770')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

# 每15分钟提交当前温度湿度数据
def postData():
    try:
        header_data = { "content-type": 'application/json; charset=utf-8', "devicetype": '1'}
        json_date = '{"device_id": "esp32_01", "json_data":{"Temperature": "' + str(round(sensor.temperature, 2)) + '","Humidity": "' + str(round(sensor.relative_humidity, 2)) + '"}}'
        # print(json_date)
        res = requests.post(remote_postdb_url, headers = header_data, data = json_date)
        # print(res.text)
    except:
       print("-->api 404") 

i2c = SoftI2C(scl=Pin(17), sda=Pin(16))
# 扫描I2C设备
print('Scan i2c bus...')
devices = i2c.scan()
if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))
  for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))

sensor = ahtx0.AHT10(i2c)         # 温湿度传感器
oled = SSD1306_I2C(128, 32, i2c)  # OLED显示屏
do_connect()

# 启动定时器
timer = Timer(1)
timer.init(period=60000*15, mode=Timer.PERIODIC, callback=lambda t:postData())

while(1):
  oled.fill(0)
  oled.show()
  temperature = str(round(sensor.temperature, 2))
  humidity = str(round(sensor.relative_humidity, 2))
  oled.text(temperature,0,0,16)
  oled.show()
  time.sleep(5)

'''
while(1):
    time.sleep(5)
    try:
        res = requests.get(url='http://192.168.0.116:8082/think/user/hello')
        print(res.text)
    except:
       print("-->api 404") 
    print("\nTemperature: %0.2f C" % sensor.temperature)
    print("Humidity: %0.2f %%" % sensor.relative_humidity)
    print('waiting...')
'''


import time
import network
import ujson
import ahtx0
import urequests as requests
import tm1637
from machine import Pin, SoftI2C, Timer, RTC

tm = tm1637.TM1637(clk=Pin(5), dio=Pin(4))

WIFI_SSD = 'MiWiFi'     # WIFI名称
WIFI_PSD = '07422770'   # WIFI密码
wlan = network.WLAN(network.STA_IF)

REMOTE_CONFIG_URL = 'http://120.24.188.63:8080/config'  # 获取配置地址
REMOTE_POSTDB_URL = 'http://120.24.188.63:8080/post'    # 接收数据地址

TEMPERATURE = '0'       # 温度
HUMIDITY = '0'          # 湿度
now_time = '    '
OledDisplay = 'OFF'
# RELAY1 = false          # 继电器1状态

THFILE = 'thfile.txt'   # 温湿度离线文件 无网络时保存数据到离线文件
GPSFILE = 'gpsfile.txt' # GPS离线文件

rtc = RTC()
rtc.init((2024, 6, 1, 5, 22, 45, 50, 0))

# 连接无线网络
def do_connect():
  wlan.active(True)
  if not wlan.isconnected():
    print('Connecting to Network... WIFI_SSD:' + WIFI_SSD)
    wlan.connect(WIFI_SSD, WIFI_PSD)
    while not wlan.isconnected():
      pass
  print('Network Config:', wlan.ifconfig())

# 每13分钟提交当前温度湿度数据
def postData():
  if wlan.isconnected():
    try:
      header_data = { "content-type": 'application/json; charset=utf-8', "devicetype": '1'}
      json_date = '{"device_id": "esp32_01", "json_data":{"Temperature": "' + str(round(sensor.temperature, 2)) + '","Humidity": "' + str(round(sensor.relative_humidity, 2)) + '"}}'
      # print(json_date)
      res = requests.post(REMOTE_POSTDB_URL, headers = header_data, data = json_date)
      # print(res.text)
    except:
      print("-->postData api 404")
  else: 
    # 无网络时重新连接网络并保存数据到离线文件
    do_connect()

# 每1分钟获取配置数据
def getConfigData():
  global now_time
  global OledDisplay
  if wlan.isconnected():
    try:
      res = requests.get(REMOTE_CONFIG_URL)
      # print(res.text)
      config_json = ujson.loads(res.text)
      if config_json.get('time') != None:
        now_time = config_json['time'].replace(':', '', 2)
        rtc.init((2024, 6, 1, 5, int(now_time[0:2]), int(now_time[2:4]), int(now_time[4:6]), 0))
      if config_json.get('OledDisplay') != None:
        OledDisplay = config_json['OledDisplay']
    except:
      print("-->getConfigData api 404") 
  else: 
    # 无网络时重新连接网络
    do_connect()

def oledDisplay():
  tm.show(str(rtc.datetime()[4]) + '.' + str(rtc.datetime()[5]) + '.' + str(rtc.datetime()[6]), True)
  time.sleep(1)
    

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
# oled = SSD1306_I2C(128, 32, i2c)  # OLED显示屏
do_connect()
getConfigData()

# 启动定时器
timer1 = Timer(1)
timer1.init(period=60000*20, mode=Timer.PERIODIC, callback=lambda t:postData())
timer2 = Timer(2)
timer2.init(period=60000, mode=Timer.PERIODIC, callback=lambda t:getConfigData())


while(1):
  #print(str(rtc.datetime()[4]) + '.' + str(rtc.datetime()[5]) + '.' + str(rtc.datetime()[6]))
  h = ''
  m = ''
  s = ''
  if rtc.datetime()[4] < 10:
    h = '0'
  if rtc.datetime()[5] < 10:
    m = '0'
  if rtc.datetime()[6] < 10:
    s = '0'
  tm.show(h + str(rtc.datetime()[4]) + m + str(rtc.datetime()[5]) + s + str(rtc.datetime()[6]), True)
  #tm.write([0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D])
  time.sleep(1)
  


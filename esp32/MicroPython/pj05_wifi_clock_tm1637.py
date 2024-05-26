# WIFI 获取时间并显示到TM1637数码管
import tm1637
import time
import network
import ujson
import urequests as requests
from machine import Pin, Timer

tm = tm1637.TM1637(clk=Pin(5), dio=Pin(4))

WIFI_SSD = 'MiWiFi'     # WIFI名称
WIFI_PSD = '07422770'   # WIFI密码
now_time = '888888'
wlan = network.WLAN(network.STA_IF)

REMOTE_CONFIG_URL = 'http://120.24.188.63:8080/config'  # 获取配置地址
REMOTE_POSTDB_URL = 'http://120.24.188.63:8080/post'    # 接收数据地址

# 连接无线网络
def do_connect():
  wlan.active(True)
  if not wlan.isconnected():
    print('Connecting to Network... WIFI_SSD:' + WIFI_SSD)
    wlan.connect(WIFI_SSD, WIFI_PSD)
    while not wlan.isconnected():
      pass
  print('Network Config:', wlan.ifconfig())

def getConfigData():
  global now_time
  if wlan.isconnected():
    try:
      res = requests.get(REMOTE_CONFIG_URL)
      # print(res.text)
      config_json = ujson.loads(res.text)
      if config_json.get('time') != None:
        now_time = config_json['time'].replace(':', '', 2)
    except:
      print("-->getConfigData api 404") 
  else: 
    # 无网络时重新连接网络
    do_connect()

timer = Timer(1)
timer.init(period=60000, mode=Timer.PERIODIC, callback=lambda t:getConfigData())

do_connect()
getConfigData()
while(1):
    tm.show(now_time, True)
    time.sleep(15)


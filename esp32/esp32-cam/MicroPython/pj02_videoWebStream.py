'''
用 MicroPython 控制 ESP32-CAM 的摄像头，运行一个实时视频，可以使用浏览器莱观看结果，架构设计如下图所示，
先让 ESP32-CAM 跟电脑先连上同一个AP(子网络），接著在 ESP32-CAM 上运行一个Web服务器，
是使用 microdot 这个包来简化架站的功能，接著打开web浏览器即可观看结果。
'''

'''
# 测试 架构 Web 服务器
# 成功将输出 ： Starting sync server on 0.0.0.0:5000...
from microdot import Microdot
app = Microdot()

@app.route('/')
def index(request):
    return 'Hello, world Microdot!'

app.run(debug=True)

'''

'''
# 开户实时视频
1-5：导入需要的模块，只有 microdot 需要额外安装，其他的都是内建模块。
7-15：连线到AP的函数定义，12行务必修改为自己的 SSID 跟 PASSWORD。
17：连线到 Wi-Fi AP
18：建立 Microdot 网站服务器
21-31：激活摄像头（camera）。
33-44：定义网站根目录(/)网页
46-57：定义视频流的路径(‘/video_feed’)与操作，这里就是整个视频流的主要代码
61：激活网站服务器
'''

from microdot import Microdot
import time
import camera
from machine import reset
import network

def connect():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  SSID = 'MiWiFi'
  PASSWORD = '07422770'
  if not wlan.isconnected():
      print('connecting to network...')
      wlan.connect(SSID, PASSWORD)
      while not wlan.isconnected():
          pass
  print('network config: ', wlan.ifconfig())

connect()
app = Microdot()

# wait for camera ready
for i in range(5):
    cam = camera.init()
    print("Camera ready?: ", cam)
    if cam:
        print("Camera ready")
        break
    else:
        time.sleep(2)
else:
    print('Timeout')
    reset()
    
@app.route('/')
def index(request):
    return '''<!doctype html>
<html>
  <head>
    <title>Microdot Video Streaming</title>
  </head>
  <body>
    <h1>Microdot Video Streaming</h1>
    <img src="/video_feed" width="30%">
  </body>
</html>''', 200, {'Content-Type': 'text/html'}

@app.route('/video_feed')
def video_feed(request):
    def stream():
        yield b'--frame\r\n'
        while True:
            frame = camera.capture()
            yield b'Content-Type: image/jpeg\r\n\r\n' + frame + \
                b'\r\n--frame\r\n'
            #time.sleep_ms(50)

    return stream(), 200, {'Content-Type': 'multipart/x-mixed-replace; boundary=frame'}

if __name__ == '__main__':
    app.run(debug=True)


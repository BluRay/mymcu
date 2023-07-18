'''
�� MicroPython ���� ESP32-CAM ������ͷ������һ��ʵʱ��Ƶ������ʹ����������ۿ�������ܹ��������ͼ��ʾ��
���� ESP32-CAM ������������ͬһ��AP(�����磩�������� ESP32-CAM ������һ��Web��������
��ʹ�� microdot ��������򻯼�վ�Ĺ��ܣ�������web��������ɹۿ������
'''

'''
# ���� �ܹ� Web ������
# �ɹ������ �� Starting sync server on 0.0.0.0:5000...
from microdot import Microdot
app = Microdot()

@app.route('/')
def index(request):
    return 'Hello, world Microdot!'

app.run(debug=True)

'''

'''
# ����ʵʱ��Ƶ
1-5��������Ҫ��ģ�飬ֻ�� microdot ��Ҫ���ⰲװ�������Ķ����ڽ�ģ�顣
7-15�����ߵ�AP�ĺ������壬12������޸�Ϊ�Լ��� SSID �� PASSWORD��
17�����ߵ� Wi-Fi AP
18������ Microdot ��վ������
21-31����������ͷ��camera����
33-44��������վ��Ŀ¼(/)��ҳ
46-57��������Ƶ����·��(��/video_feed��)��������������������Ƶ������Ҫ����
61��������վ������
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


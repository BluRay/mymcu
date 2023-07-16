# https://doc.itprojects.cn/0006.zhishi.esp32/02.doc/index.html#/e01.cam

import camera

# ��ʼ������ͷ
try:
    camera.init(0, format=camera.JPEG)
except Exception as e:
    camera.deinit()
    camera.init(0, format=camera.JPEG)
#camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)

# ����һ��ͼƬ
buf = camera.capture()  # ��С��640x480

# ����ͼƬ���ļ�
with open("2.png", "wb") as f:
    f.write(buf)  # buf�е����ݾ���ͼƬ�����ݣ�����ֱ��д�뵽�ļ�������
    print("camera.capture SUCCESS!")
camera.deinit()
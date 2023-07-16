# https://doc.itprojects.cn/0006.zhishi.esp32/02.doc/index.html#/e01.cam

import camera

# 初始化摄像头
try:
    camera.init(0, format=camera.JPEG)
except Exception as e:
    camera.deinit()
    camera.init(0, format=camera.JPEG)
#camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)

# 拍摄一张图片
buf = camera.capture()  # 大小是640x480

# 保存图片到文件
with open("2.png", "wb") as f:
    f.write(buf)  # buf中的数据就是图片的数据，所以直接写入到文件就行了
    print("camera.capture SUCCESS!")
camera.deinit()
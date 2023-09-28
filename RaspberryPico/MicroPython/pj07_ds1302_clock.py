# TODO ds1302 时钟模块
# 设置当前时间 读取时间显示到墨水屏【EPD_2in9_B】
# https://blog.csdn.net/weixin_52168861/article/details/125212859
# https://github.com/LNfromNorth/DesktopClock/tree/main/OtherPy/DS1302
from DS1302 import DS1302

ds1302 = DS1302(0,1,2)
ds1302.SetTime(22,6,8,22,15,00,3)
date = ds1302.Now()
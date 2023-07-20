# 通过蓝牙控制墨水屏显示
import uos
import machine
import utime
import random
from EPD_2in9_B import EPD_2in9_B
from font64 import font64

KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]
epd = EPD_2in9_B()

def showstr(font, index, font_num, col_num, start, font_width):
    # font: 待显示的字符
    # index：第几个字符 	font_num：共多少字符 所有字符显示完后刷新
    # col_num： 第几行 0，1
    # start： 起始位置 	font_width：字符宽度 中文=8 英文数字 = 4
    font_size = 64	# 字符像素高度
    rect_list = [] * font_size
    for i in range(font_size):
        rect_list.append([0x00] * font_size)
    #print(rect_list)
    for c in range(font_width):	# 列
        for k in range(font_size):
            row_list = rect_list[k]
            for i in range(8):
                flag = KEYS[i] & font[c][k]
                row_list[(c * 8 ) + i] = 1 if flag > 0 else 0
    i=10 + col_num*64
    for row in rect_list:
        j=296-(64//(8//font_width))*(index)-start
        for r in row:
            if r:
                epd.imagered.pixel(i, j, 0x00)
            j=j-1
        i=i+1
    if (index + 1 == font_num):
        epd.display()
        epd.delay_ms(2000)

print(uos.uname())      #列出開發板的資訊
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(16), rx=machine.Pin(17))
print(uart)

led = machine.Pin(25, machine.Pin.OUT)	# 处理蓝牙命令时亮灯
led.value(0)
rxData = bytes()

'''
strlist = []
strlist = font64.getChar(font64)
i=0
for font in strlist:
    showstr(font,i)
    i=i+1
'''    
uart.write('ready')
while True:
    if uart.any():
        rxData = uart.readline()
        #uart.write(cmd)
        print(str(rxData).replace("b\'\\x","").replace('\'',''))
        if (rxData == b'\x00'):		# 清屏
            led.value(1)
            epd.Clear(0xff, 0xff)
            epd.imageblack.fill(0xff)
            epd.imagered.fill(0xff)
            uart.write('clear done')
            led.value(0)
        
        if (rxData == b'\x01'):		# 
            led.value(1)
            uart.write('led open')
        if (rxData == b'\x02'):		# 
            led.value(0)
            uart.write('led close')
            
        if (rxData == b'\x99'):		# 随机算术
            led.value(1)
            epd.Clear(0xff, 0xff)
            epd.imageblack.fill(0xff)
            epd.imagered.fill(0xff)
            chars1 = [str(random.randint(31,39)),'2B',str(random.randint(31,39)),'3D']
            strlist1 = font64.getstr(font64, chars1)
            i=0
            for font in strlist1:
                showstr(font,i,len(strlist1),0,64*1,4)
                i=i+1
            led.value(0)
            
        if (rxData == b'\x88'):		# 显示名字
            led.value(1)
            uart.write('show name start')
            epd.Clear(0xff, 0xff)
            epd.imageblack.fill(0xff)
            epd.imagered.fill(0xff)
            chars = ['D1EE','D2BB','E9AA']
            chars1 = ['31','35','32']
            chars2 = ['37','34','38','38','2D','38','31','34','35']
            #strlist = font64.getChar(font64)
            strlist = font64.getstr(font64, chars)
            i=0
            for font in strlist:
                showstr(font,i,len(strlist),0,0,8)
                i=i+1
                
            strlist1 = font64.getstr(font64, chars1)
            i=0
            for font in strlist1:
                showstr(font,i,len(strlist1),0,64*3,4)
                i=i+1
                
            strlist2 = font64.getstr(font64, chars2)
            i=0
            for font in strlist2:
                showstr(font,i,len(strlist2),1,0,4)
                i=i+1
            
            uart.write('show name done')
            led.value(0)
            

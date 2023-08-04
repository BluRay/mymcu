# 20230717
# 4*4矩阵键盘实现
'''
程序设计上通常采用逐行逐列进行扫描，4*4的矩阵键盘一共需要8个单片机的GPIO引脚，
将控制行的引脚设置成输出，控制列的引脚设置成输入上拉。
先扫描第一行，那么就将PD0~PD2输出高电平，将PD3输出低电平，记为0xF7,行确定好后，
开始扫描列，控制列的引脚为输入引脚，将其和0XF7相与，如果哪一位为0，那么就证明哪一个被按下。
按键没有被按下的时候，IO口的状态为 **1111 0000 ，**扫描第一行将PD3输出低电平，其他行输出高电平，即为1111 0111，
假设第一个按键被按下，那么此时PD4引脚读到低电平，那么读到的引脚变
'''

# TODO 
import time
import RPi.GPIO as GPIO
class keypad(object):
  KEYPAD=[
    ['1','2','3','A'],
    ['4','5','6','B'],
    ['7','8','9','C'],
    ['*','0','#','D']]
 
  ROW    =[12,16,20,21]#行
  COLUMN =[6,13,19,26]#列
 
#初始化函数
def __init__():
  GPIO.cleanup()
  GPIO.setmode(GPIO.BCM)
#取得键盘数函数
def getkey():
	GPIO.setmode(GPIO.BCM)
#设置列输出低
  for i in range(len(keypad.COLUMN)):
    GPIO.setup(keypad.COLUMN[i],GPIO.OUT)
    GPIO.output(keypad.COLUMN[i],GPIO.LOW)
#设置行为输入、上拉
  for j in range(len(keypad.ROW)):
    GPIO.setup(keypad.ROW[j],GPIO.IN,pull_up_down=GPIO.PUD_UP)
 
#检测行是否有键按下，有则读取行值
  RowVal=-1
  for i in range(len(keypad.ROW)):
    RowStatus=GPIO.input(keypad.ROW[i])
    if RowStatus==GPIO.LOW:
       RowVal=i
       #print('RowVal=%s' % RowVal)
#若无键按下,则退出，准备下一次扫描
  if RowVal<0 or RowVal>3:
    exit()
    return
 
#若第RowVal行有键按下，跳过退出函数，对掉输入输出模式
#第RowVal行输出高电平，
  GPIO.setup(keypad.ROW[RowVal],GPIO.OUT)
  GPIO.output(keypad.ROW[RowVal],GPIO.HIGH)
#列为下拉输入
  for j in range(len(keypad.COLUMN)):
    GPIO.setup(keypad.COLUMN[j],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
 
#读取按键所在列值
  ColumnVal=-1
  for i in range(len(keypad.COLUMN)):
    ColumnStatus=GPIO.input(keypad.COLUMN[i])
    if ColumnStatus==GPIO.HIGH:
      ColumnVal=i
#等待按键松开
      while GPIO.input(keypad.COLUMN[i])==GPIO.HIGH:
        time.sleep(0.05)
        #print ('ColumnVal=%s' % ColumnVal)
#若无键按下，返回
  if ColumnVal<0 or ColumnVal>3:
    exit()
    return
 
  exit()
  return keypad.KEYPAD[RowVal][ColumnVal]
 
def exit():
 
  import RPi.GPIO as GPIO
  for i in range(len(keypad.ROW)):
    GPIO.setup( keypad.ROW[i],GPIO.IN,pull_up_down=GPIO.PUD_UP)
  for j in range(len( keypad.COLUMN)):
    GPIO.setup( keypad.COLUMN[j],GPIO.IN,pull_up_down=GPIO.PUD_UP)
 
key=None
 
while True:
  key=getkey()
  if not key==None:
    print ('You enter the  key:',key)
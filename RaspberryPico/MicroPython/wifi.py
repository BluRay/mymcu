# TODO
# 树莓派Pico与ESP01S无线WiFi模块
# 采用树莓派Pico开发板UART1串口，这里使用Pin6(物理引脚6)UART1 TX串行通信发送数据线信号线和Pin9(物理引脚12)UART1 RX串行通信接收数据信号线
# https://blog.csdn.net/yuanzywhu/article/details/122626070
''' 
ESP01S无线WiFi模块基于ESP8266芯片，其主要特性如下：
•工作电压：+3.3 V(官方手册给出的外接电源参数：2.7V~3.6V，Imax>500mA)
•接口：可使用AT命令与UART串口进行串行通信
•集成TCP/IP协议栈
•802.11 b/g /n通信协议
•使用时无须接外部元件
ESP01S模块通过其TX和RX串口引脚与树莓派Pico进行通信，ESP01S模块接口信号引脚说明如下：
(1) VCC：3.3V电源
(2) GND：接地
(3) GPIO0-Flash：GPIO引脚，将该引脚连接到+3.3V为运行模式，连接到GND为下载模式
(4) GPIO2：GPIO引脚
(5) RST/GPIO16：复位引脚(若使用ESP01模块，运行模式须将该引脚上拉接；若使用ESP01S模块，运行模式可将该引脚悬空)
(6) EN/CH_PD：芯片使能引脚(若使用ESP01模块，运行模式须将该引脚上拉接；若使用ESP01S模块，运行模式可将该引脚悬空)
(7) TX/GPIO0：串行数据发送信号
(8) RX/GPIO3：串行数据接收信号
从ESP01S无线WiFi模块知，ESP-01S无线WiFi模块供电电压范围为2.7V-3.6V，最大电流Imax>500mA。树莓派Pico硬件接口扩展引脚3V3(OUT)为3.3V直流电源，我们可用该直流电源对ESP-01S无线WiFi模块进行供电，但该电源最大输出电流仅有300mA。为确保系统工作更加稳定可靠，这里采用带开关电池盒的两节5号电池串联对ESP01S无线WiFi模块进行供电(见图2)。当然，我们也可直接用3.0V-3.6V直流稳压电源对ESP01S供电，或者将4.75V-12V 直流稳压电源(如5V直流电压)连接到ASM1117三端稳压器模块的输入端在输出端产生3.3V电源对ESP-01S进行供电等(ASM1117：输入电压范围4.75V~12V, 输出电压3.3V)。
在图2中，树莓派Pico扩展口与ESP01S无线WiFi连接信号如下：Pico UART1 RX与ESP01S TX连接，Pico UART1 TX与ESP01S RX连接，Pico GND、ESP01S GND都和电池盒电源的负极(黑线)共地连接，ESP01S VCC与电池盒电源的正极(红线)连接。
设Pico UART1串口通信速率为115200 bps，采用MicroPython对Pico UART1串口进行初始化设置的程序片段如下：

2、ESP01S无线WiFi模块使用方法
(1) ESP01S连接WiFi
ESP01S连接WiFi，也就是上网用的无线信号，假设当前现场使用的无线信号(网络热点ssid)为H3C_202，密码(psw)为abcde12345。使用AT命令。
Step 1： AT+RST。ESP01S复位，延时不少于2s。
Step 2：AT+CWMODE=1。设置Station模式，需延时不少于2.5s。
Step 3：AT+CIPMUX=0。设置单路连接模式，延时不少于1s。
Step 4：AT+CWJAP=”H3C_202”,”abcde12345”。连接WiFi延时时间要长一些，建议测试延时不少于8秒。
'''
#------------------------------------------------------
# 基于树莓派Pico和ESP01S无线WiFi模块的通信程序示例
#------------------------------------------------------
from machine import Pin, UART
import utime
uart1 = UART(1,baudrate=115200,rx=Pin(9),tx=Pin(4))   #ESP01S出厂时的波特率为115200(OR UART0:0,1,0)
LED = Pin(25, Pin.OUT)
LED.value(1)
utime.sleep(1)
LED.value(0)
# 定义树莓派Pico+ESP01S无线模块连接到WiFi函数
# 向树莓派Pico的ESP01S无线模块发送AT命令，连接到本地可用的WiFi
def ConnectToWiFi():
    uart1.write("AT+RST\r\n")         # 复位ESP01S无线模块
    utime.sleep(2)
 
    uart1.write("AT+CWMODE=1\r\n")    # 使用Station模式
    utime.sleep(3)
      
    uart1.write("AT+CIPMUX=0\r\n")    # 0:使用单连接模式
    utime.sleep(1)
    
    uart1.write('''AT+CWJAP="H3C_202","abcde12345"\r\n''')
    # 连接网络热点，ssid：H3C_202, psw：abcde12345
    utime.sleep(10)    # 延时10s
    
    # uart1.write("AT+CWLAP")    # 不是必须
    # utime.sleep(1)
    uart1.write('''AT+CIPSTART="UDP","192.168.124.2",5000,5000,2\r\n''')
    # 192.168.124.2为本人智能手机使用的IP地址
    # 192.168.124.6为Pico+ESP01使用的IP地址
    utime.sleep(4)
ConnectToWiFi()
# 执行循环主程序
while True:
    if uart1.any():   # 判断是否有数据可以接收
        buffer = uart1.readline()       # 读取字符串数据
        data = buffer.decode('utf-8')   # 以UTF-8编码格式对buffer字符串进行解码
        print(data)
    if data.find("开灯")>0:    # 若查找接收到的字符串为"开灯",则Pico板载LED点亮(未找到返回-1)
        LED.value(1)
    if data.find("关灯")>0:   # 若查找接收到的字符串为"关灯",则Pico板载LED熄灭(未找到返回-1)
        LED.value(0)


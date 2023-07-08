import uos
import machine
import utime

print(uos.uname())     # 列出開發板的資訊
uart = machine.UART(1, baudrate=9600, tx=machine.Pin(8), rx=machine.Pin(9))  # Pin(xx) = GPxx
print(uart)            # 串口信息
rxData = bytes()
while True:
    if uart.any():
        rxData = uart.readline()
        #uart.write(cmd)
        print(rxData)

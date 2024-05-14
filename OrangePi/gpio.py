import OPi.GPIO as GPIO
from time import sleep
# BOARD编号方式，基于插座引脚编号
GPIO.setmode(GPIO.BOARD)
# 输出模式
GPIO.setup(7, GPIO.OUT)
try:
   while True:
      GPIO.output(7, GPIO.HIGH)
      sleep(1)
      print("LED RED ON \t\t  \r", end = "")	
      GPIO.output(7, GPIO.LOW)
      sleep(1)
      print("LED RED OFF \t\t  \r", end = "")	    
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
   print("Keyboard interrupt")
except:
   print("some error") 
finally:
   print("clean up") 
   GPIO.cleanup() # cleanup all GPIO 
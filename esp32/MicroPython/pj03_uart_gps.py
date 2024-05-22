# https://microcontrollerslab.com/neo-6m-gps-module-esp32-micropython/

from machine import Pin, UART, SoftI2C
from ssd1306 import SSD1306_I2C

import utime, time

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)     #initializing the I2C method for ESP32

oled = SSD1306_I2C(128, 64, i2c)

gpsModule = UART(2, baudrate=9600)
print(gpsModule)

buff = bytearray(255)

TIMEOUT = False
FIX_STATUS = False

latitude = ""
longitude = ""
satellites = ""
GPStime = ""

def getGPS(gpsModule):
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, GPStime
    
    timeout = time.time() + 8 
    while True:
        gpsModule.readline()
        buff = str(gpsModule.readline())
        parts = buff.split(',')
    
        if (parts[0] == "b'$GPGGA" and len(parts) == 15):
            if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                print(buff)
                
                latitude = convertToDegree(parts[2])
                if (parts[3] == 'S'):
                    latitude = -latitude
                longitude = convertToDegree(parts[4])
                if (parts[5] == 'W'):
                    longitude = -longitude
                satellites = parts[7]
                GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                FIX_STATUS = True
                break
                
        if (time.time() > timeout):
            TIMEOUT = True
            break
        utime.sleep_ms(500)
        
def convertToDegree(RawDegrees):

    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return str(Converted)
    
    
while True:
    
    getGPS(gpsModule)

    if(FIX_STATUS == True):
        print("Printing GPS data...")
        print(" ")
        print("Latitude: "+latitude)
        print("Longitude: "+longitude)
        print("Satellites: " +satellites)
        print("Time: "+GPStime)
        print("----------------------")
        
        oled.fill(0)
        oled.text("Lat: "+latitude, 0, 0)
        oled.text("Lng: "+longitude, 0, 10)
        oled.text("Satellites: "+satellites, 0, 20)
        oled.text("Time: "+GPStime, 0, 30)
        oled.show()
        
        FIX_STATUS = False
        
    if(TIMEOUT == True):
        print("No GPS data is found.")
        TIMEOUT = False
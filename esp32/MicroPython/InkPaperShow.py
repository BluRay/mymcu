'''
For Pico_ePaper-2.9-B
EPD		=>		Esp32-C3
VCC		->		3_VSYS
GND		->		2_GND
DIN		->		8
CLK		->		7
CS		->		6
DC		->		5
RST		->		4
BUSY	->		3
'''
from machine import Pin, SPI
import framebuf
import utime

# Display resolution
EPD_WIDTH       = 128
EPD_HEIGHT      = 296

RST_PIN         = 4
DC_PIN          = 5
CS_PIN          = 6
BUSY_PIN        = 3
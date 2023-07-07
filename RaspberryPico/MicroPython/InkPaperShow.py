'''
For Pico_ePaper-2.9-B
EPD		=>		Pico
VCC		->		VSYS
GND		->		GND
DIN		->		11
CLK		->		10
CS		->		9
DC		->		8
RST		->		12
BUSY		->		13
'''

from machine import Pin, SPI
import framebuf
import utime

# Display resolution
EPD_WIDTH       = 128
EPD_HEIGHT      = 296

RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13


KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]
# 杨 宋体 64*64 8列
font1 = [[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1f, 0x0f, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x03, 0x03, 0x07, 0x07, 0x0f, 0x0e, 0x1c, 0x3c, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0xff, 0xff, 0x03, 0x07, 0x07, 0x07, 0x07, 0x0f, 0x0f, 0x0f, 0x1f, 0x1f, 0x1f, 0x3f, 0x3f, 0x3f, 0x7f, 0x7f, 0xfb, 0xfb, 0xf3, 0xe3, 0xe3, 0xc3, 0x83, 0x83, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x80, 0xe0, 0xf8, 0xf8, 0xf0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe1, 0xe3, 0xff, 0xff, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xf8, 0xfe, 0xff, 0xff, 0xff, 0xef, 0xe7, 0xe7, 0xe3, 0xe3, 0xe1, 0xe1, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe3, 0xe7, 0xe7, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe3, 0xe3, 0xe0, 0xe0, 0xe0, 0x80, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0x1f, 0x0f, 0x00, 0x00, 0x00, 0xc0, 0xe0, 0xf0, 0xf8, 0xfc, 0x00, 0x00, 0x00, 0x00, 0x01, 0x03, 0x07, 0x1f, 0x1f, 0x0f, 0xc7, 0xc2, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xc1, 0xc1, 0x03, 0x07, 0x0f, 0x1f, 0x3f, 0x7c, 0xf8, 0xf0, 0xc0, 0x00, 0x00, 0x00, 0x01, 0x03, 0x0f, 0x1f, 0x3e, 0xfc, 0xf0, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x03, 0x0f, 0x1f, 0x3f, 0x7f, 0xfe, 0xfc, 0xf8, 0xf0, 0xff, 0xff, 0x8f, 0x0f, 0x1f, 0x1f, 0x3f, 0x7e, 0x7c, 0xfc, 0xf8, 0xf0, 0xf0, 0xe0, 0xc0, 0x81, 0x03, 0x07, 0x07, 0x0f, 0x1f, 0x3f, 0x7e, 0xfc, 0xf8, 0xf0, 0xc0, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0xff, 0xff, 0x07, 0x0f, 0x1f, 0x3f, 0x7e, 0xfc, 0xf8, 0xf0, 0xe0, 0xc0, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xc3, 0x87, 0x87, 0x0f, 0x0f, 0x0f, 0x1f, 0x1f, 0x3f, 0x7e, 0x7e, 0xfc, 0xfc, 0xf8, 0xf0, 0xe0, 0xe0, 0xc0, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf8, 0xff, 0x3f, 0x0f, 0x07, 0x03, 0x03, 0x00, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0xe0, 0xf0, 0xf8, 0xfc, 0xf8, 0xe0, 0xc0, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x03, 0xff, 0xff, 0xe3, 0xe3, 0xe3, 0xc3, 0xc3, 0x87, 0x87, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x1f, 0x1f, 0x1f, 0x3f, 0x7f, 0xff, 0xfe, 0xfe, 0xfc, 0xf8, 0xe0, 0x00, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0xe0, 0xf8, 0xf8, 0xf0, 0xe0, 0xe0, 0xe0, 0xe0, 0xc0, 0xc0, 0xc0, 0xc0, 0xc0, 0xc0, 0xc0, 0xc0, 0xc0, 0xc0, 0xc0, 0xc0, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]]
# 一 宋体 64*64 8列
font2 = [[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1f, 0x1f, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x0f, 0x1f, 0x3f, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x80, 0xc0, 0xe0, 0xf0, 0xf8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]]

# 楠 宋体 64*64 8列
font3 = [[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1f, 0x1f, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x03, 0x03, 0x07, 0x07, 0x0f, 0x0f, 0x1e, 0x1c, 0x3c, 0x38, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
[0x00, 0x00, 0x0e, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0xff, 0xff, 0xcf, 0x0f, 0x0f, 0x0f, 0x1f, 0x1f, 0x1f, 0x1f, 0x3f, 0x3f, 0x3f, 0x7f, 0x7f, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xef, 0xef, 0xcf, 0x8f, 0x8f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0e, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x80, 0xe0, 0xe0, 0xc0, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x8c, 0x9e, 0xbf, 0xff, 0xff, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0xe0, 0xf8, 0xfe, 0xff, 0xbf, 0x9f, 0x9f, 0x8f, 0x8f, 0x8f, 0x86, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x00, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0x7e, 0x00, 0x00, 0x80, 0xc0, 0x00, 0x20, 0x38, 0x3f, 0x3f, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0xbe, 0xbe, 0xbe, 0x3e, 0x3e, 0x3e, 0x3f, 0x3f, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3f, 0x3f, 0x3f, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x38, 0x00, 0x00],
[0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0xff, 0xff, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0xff, 0xff, 0x00, 0x00, 0x60, 0x78, 0x7c, 0x3e, 0x3f, 0x1f, 0x1f, 0x1f, 0x0f, 0x0e, 0xff, 0xff, 0xfd, 0x01, 0x01, 0x01, 0x01, 0x01, 0xff, 0xff, 0xf9, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
[0x00, 0x00, 0x80, 0xe0, 0xfc, 0xfc, 0xf8, 0xf0, 0xf0, 0xf0, 0xf0, 0xf0, 0xff, 0xff, 0xf0, 0xf0, 0xf0, 0xf0, 0xf0, 0xf0, 0xf0, 0xf0, 0xff, 0xff, 0x00, 0x0c, 0x0f, 0x0f, 0x0f, 0x1f, 0x1f, 0x1e, 0x3e, 0x3c, 0x3d, 0x7b, 0xff, 0xff, 0xf0, 0xf0, 0xf0, 0xf0, 0xf0, 0xf1, 0xff, 0xff, 0xf0, 0xf0, 0xf0, 0xf0, 0xf0, 0xf0, 0xf0, 0xf0, 0xf0, 0xf7, 0xf7, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x03, 0x07, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x03, 0xff, 0xff, 0x03, 0x03, 0x03, 0xc3, 0xe3, 0x83, 0x03, 0x03, 0x03, 0x03, 0xe3, 0xf3, 0xfb, 0xff, 0x03, 0x03, 0x03, 0x03, 0xf3, 0xfb, 0xff, 0xff, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0xff, 0xff, 0xff, 0x3f, 0x1f, 0x0f, 0x0c, 0x00, 0x00],
[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0xc0, 0xe0, 0xf0, 0xf8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0xe0, 0xf0, 0xf8, 0xf0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xe0, 0xc0, 0x80, 0x00, 0x00, 0x00, 0x00]]

size = 64	# 字体大小 8|16|64

class EPD_2in9_B:
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        
        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)
        
        self.buffer_black = bytearray(self.height * self.width // 8)
        self.buffer_red = bytearray(self.height * self.width // 8)
        self.imageblack = framebuf.FrameBuffer(self.buffer_black, self.width, self.height, framebuf.MONO_HLSB)
        self.imagered = framebuf.FrameBuffer(self.buffer_red, self.width, self.height, framebuf.MONO_HLSB)
        self.init()

    def digital_write(self, pin, value):
        pin.value(value)

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def module_exit(self):
        self.digital_write(self.reset_pin, 0)

    # Hardware reset
    def reset(self):
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)


    def send_command(self, command):
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([command])
        self.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([data])
        self.digital_write(self.cs_pin, 1)
        
    def send_data1(self, buf):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray(buf))
        self.digital_write(self.cs_pin, 1)
        
    def ReadBusy(self):
        print('busy')
        self.send_command(0x71)
        while(self.digital_read(self.busy_pin) == 0): 
            self.send_command(0x71)
            self.delay_ms(10) 
        print('busy release')
        
    def TurnOnDisplay(self):
        self.send_command(0x12)
        self.ReadBusy()

    def init(self):
        print('init')
        self.reset()
        self.send_command(0x04)  
        self.ReadBusy()#waiting for the electronic paper IC to release the idle signal

        self.send_command(0x00)    #panel setting
        self.send_data(0x0f)   #LUT from OTP,128x296
        self.send_data(0x89)    #Temperature sensor, boost and other related timing settings

        self.send_command(0x61)    #resolution setting
        self.send_data (0x80)  
        self.send_data (0x01)  
        self.send_data (0x28)

        self.send_command(0X50)    #VCOM AND DATA INTERVAL SETTING
        self.send_data(0x77)   #WBmode:VBDF 17|D7 VBDW 97 VBDB 57
                            # WBRmode:VBDF F7 VBDW 77 VBDB 37  VBDR B7
        return 0       
        
    def display(self):
        self.send_command(0x10)
        self.send_data1(self.buffer_black)
                
        self.send_command(0x13)
        self.send_data1(self.buffer_red)   

        self.TurnOnDisplay()

    
    def Clear(self, colorblack, colorred):
        self.send_command(0x10)
        self.send_data1([colorblack] * self.height * int(self.width / 8))
                
        self.send_command(0x13)
        self.send_data1([colorred] * self.height * int(self.width / 8))
        
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0X02) # power off
        self.ReadBusy()
        self.send_command(0X07) # deep sleep
        self.send_data(0xA5)
        
        self.delay_ms(2000)
        self.module_exit()
        
        
if __name__=='__main__':
    epd = EPD_2in9_B()
    epd.Clear(0xff, 0xff)
    epd.imageblack.fill(0xff)
    epd.imagered.fill(0xff)
    '''
    epd.imageblack.text("Waveshare", 0, 10, 0x00)
    epd.imagered.text("ePaper-2.9-B", 0, 25, 0x00)
    epd.imageblack.text("RPi Pico", 0, 40, 0x00)
    epd.imagered.text("Hello World", 0, 55, 0x00)
    epd.display()
    epd.delay_ms(2000)
    '''
    '''
    for i in range(0, 128):
        for j in range(65, 75):
            epd.imageblack.pixel(i, j, 0x00)
        for j in range(76, 85):
            epd.imagered.pixel(i, j, 0x00)
    epd.display()
    epd.delay_ms(2000)
    '''
    font = font1
    rect_list = [] * size
    for i in range(size):
        rect_list.append([0x00] * size)
    #print(rect_list)
    for c in range(size // 8):	# 列
        for k in range(size):
            row_list = rect_list[k]
            for i in range(8):
                flag = KEYS[i] & font[c][k]
                row_list[(c * 8 ) + i] = 1 if flag > 0 else 0
    i=10
    for row in rect_list:
        j=296-64*(1-1)
        for r in row:
            if r:
                epd.imagered.pixel(i, j, 0x00)
            j=j-1
        i=i+1
    
    epd.display()
    epd.delay_ms(2000)
    
    font = font2
    rect_list = [] * size
    for i in range(size):
        rect_list.append([0x00] * size)
    #print(rect_list)
    for c in range(size // 8):	# 列
        for k in range(size):
            row_list = rect_list[k]
            for i in range(8):
                flag = KEYS[i] & font[c][k]
                row_list[(c * 8 ) + i] = 1 if flag > 0 else 0
    i=10
    for row in rect_list:
        j=296-64*(2-1)
        for r in row:
            if r:
                epd.imagered.pixel(i, j, 0x00)
            j=j-1
        i=i+1
    
    epd.display()
    epd.delay_ms(2000)
    
    font = font3
    rect_list = [] * size
    for i in range(size):
        rect_list.append([0x00] * size)
    #print(rect_list)
    for c in range(size // 8):	# 列
        for k in range(size):
            row_list = rect_list[k]
            for i in range(8):
                flag = KEYS[i] & font[c][k]
                row_list[(c * 8 ) + i] = 1 if flag > 0 else 0
    i=10
    for row in rect_list:
        j=296-64*(3-1)
        for r in row:
            if r:
                epd.imagered.pixel(i, j, 0x00)
            j=j-1
        i=i+1
    
    epd.display()
    epd.delay_ms(2000)
    
    '''
    epd.imagered.vline(10, 90, 40, 0x00)
    epd.imagered.vline(90, 90, 40, 0x00)
    epd.imageblack.hline(10, 90, 80, 0x00)
    epd.imageblack.hline(10, 130, 80, 0x00)
    epd.imagered.line(10, 90, 90, 130, 0x00)
    epd.imageblack.line(90, 90, 10, 130, 0x00)
    epd.display()
    epd.delay_ms(2000)
    
    epd.imageblack.rect(10, 150, 40, 40, 0x00)
    epd.imagered.fill_rect(60, 150, 40, 40, 0x00)
    epd.display()
    epd.delay_ms(2000)
    '''    
    #epd.Clear(0xff, 0xff)
    #epd.delay_ms(2000)
    print("sleep")
    epd.sleep()

'''
for row in rect_list:
	#print(row)
	for i in row:
         if i:
             #前景字符（即用来表示汉字笔画的输出字符）
             print('O', end=' ')
         else:
             # 背景字符（即用来表示背景的输出字符）
             print(' ', end=' ')
	print()
print("--------")
'''

# ����ݮ��Pico ���Ƶ�� https://www.eet-china.com/mp/a38406.html
# TODO

import utime
from machine import Pin

# ������������motor1a��motor1b����Щ���洢���������GPIO���źţ��Կ���DRV8833�����������
motor1a = Pin(14, Pin.OUT)
motor1b = Pin(15, Pin.OUT)

# ����һ��ʹ�綯����ǰ�����ĺ�����Ϊ�ˣ�������Ҫ��һ���������ߣ���һ���������͡���̶������ǵ�Ԥ�ڷ��򴫴�������������������Ӧ��������Ž����������ʹ������趨�����ƶ���
def forward():
	motor1a.high()
  motor1b.low()
  
# ����һ������ƶ��ĺ�������ῴ��GPIO����״̬��ת���Ӷ����µ綯�����෴������ת��
def backward():
  motor1a.low()
  motor1b.high()
  
# ����һ��ֹͣ�綯���ĺ�����ͨ�����������Ŷ����ͣ����Ǹ��ߵ綯��������ֹͣ�綯���������˶���
def stop():
  motor1a.low()
  motor1b.low()

while True:
	# TODO
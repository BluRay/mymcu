#### i2c Oled
- ����i2c: sudo raspi-config
- Luma.oled�� [Luma api](https://luma-oled.readthedocs.io/en/latest/api-documentation.html) [�̳�1](https://blog.csdn.net/qq_46476163/article/details/116395514)
- TODO

### RPi.GPIO
- https://pypi.org/project/RPi.GPIO/
- ͨ�� gpio readall �鿴������Ϣ
- ��װ�����gpio���wget https://project-downloads.drogon.net/wiringpi-latest.deb \ sudo dpkg -i wiringpi-latest.deb
![image](PI_PIN.png)
![image](PI_PIN2.png)
####GPIO������;
�����40Pin�ܽ��У�����12����Դ���⣬����28�����ǿɱ�̵�GPIO�����в���GPIO���Ը���ΪIIC��SPI��UART��PWM�ȵȣ��������������������衣

I2C����Philips��˾������һ�ּ򵥡�˫�������ͬ���������ߡ���ֻ��Ҫ�����߼����������������ϵ�����֮�䴫����Ϣ����ݮ��ͨ��I2C�ӿڿɿ��ƶ������������������ǵ�ͨ����ͨ��SDA(��������)��SCL(ʱ���ٶ�����)����ɵġ�ÿ�����豸����һ��Ψһ�ĵ�ַ������������豸�����ͨ�š�ID_EEPROM����Ҳ��I2CЭ�飬��������HATsͨ�š�

SPI�Ǵ�������ӿڣ����ڿ��ƾ������ӹ�ϵ����������ôӽ������������ӳ��ķ�ʽ��������ݮ����SPI��SCLK��MOSI��MISO�ӿ���ɣ�SCLK���ڿ��������ٶȣ�MOSI�����ݴ���ݮ�ɷ��͵������ӵ��豸����MISO���෴��

��ʹ��Arduino������һ����˵��UART��Serial��ͨ���첽��/�����ӿ����ڽ�Arduino���ӵ�Ϊ���̵ļ�����ϣ�Ҳ���������豸�� RX �� TX ����֮���ͨ�š������ݮ���� raspi-config �������˴����նˣ������ʹ����Щ����ͨ��������������ݮ�ɣ�Ҳ����ֱ�����ڿ���Arduino��

����ݮ���ϣ����е����Ŷ�����ʵ�����PWM����GPIO12��GPIO13��GPIO18��GPIO19����ʵ��Ӳ��������ơ�

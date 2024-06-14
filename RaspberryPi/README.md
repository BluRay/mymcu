### i2c Oled
- 开启i2c: sudo raspi-config
- Luma.oled库 [Luma api](https://luma-oled.readthedocs.io/en/latest/api-documentation.html) 
[教程1](https://blog.csdn.net/qq_46476163/article/details/116395514)
[教程2](https://blog.csdn.net/u011198687/article/details/120347965)
### OpenMediaVault(OMV)
[教程1](https://blog.csdn.net/qq_41676577/article/details/128063914)
[教程2](https://www.cnblogs.com/Yogile/p/12577321.html)
用到的是最新的树莓派官方精简版系统（不能使用带桌面的版本！）
安装脚本 debs/pi4b_omv_install
将树莓派通过 网线 连接到路由器上  OMV不支持WIFI传输，只可通过网线连接。
不要使用OMV系统对U盘进行擦除，可能导致U盘无法识别。应使用格式化好的U盘。
### Mysql8
```bash
docker pull mysql:8.1.0
docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=XXXXXX -d mysql:8.1.0
```
#进入容器 放开root远程登陆 Mysql 8.0版本配置方法：
```bash
docker exec -it mysql bash
create user 'root'@'%' identified by '密码';
grant all on *.* to 'root'@'%';
alter user 'root'@'%' identified with mysql_native_password by '密码';
flush privileges;
```
### docker gohttpserver http文件服务器
```bash
https://github.com/codeskyblue/gohttpserver
docker pull codeskyblue/gohttpserver
docker pull nvidhub/gohttpserver:arm64  # 树莓Pi
docker run -it --name gohttpserver -p 8082:8000 -v /opt/gohttpfileserver:/app/public codeskyblue/gohttpserver --upload --delete
```
### docker clash-mate 代理服务器
```bash
docker run -d --name clash-mate --log-opt max-size=1m -v /opt/clash/clash.yaml:/root/.config/clash/config.yaml -p 9090:9090 -p 7890:7890 metacubex/clash-meta:latest
```
### docker npc 内网穿透 image:ffdfgdfg/npc

- TODO
### ST7735 1.44 寸彩色 TFT 屏幕（SPI 通信）
[教程1](https://timor.tech/mcu/lcd/rpi-st7735-python.html)
- TODO
### RPi.GPIO
- https://pypi.org/project/RPi.GPIO/
- 通过 gpio readall 查看引脚信息
- 安装或更新gpio：https://github.com/WiringPi/WiringPi Releases下载arm64版本的deb \ sudo dpkg -i wiringpi-2.61-1-arm64.deb
![image](PI_PIN.png)
![image](PI_PIN2.png)
### 连接摄像头并通过串流远程访问
https://blog.csdn.net/weixin_45994747/article/details/109605765
硬件连接时我们首先需要使用树莓派摄像头FFC排线，连接树莓派摄像头与树莓派开发板。其中排线连接的接口被称为CSI（Camera Serial Interface）接口。
树莓派开发板的CSI接口位于USB和以太网接口旁边。我们先将CSI接口的黑色挡板拔开，之后将排线蓝色一端正对以太网接口方向插入，之后按下黑色挡板进行固定。

使用Linux下一款开源监控软件：motion
####GPIO引脚用途
在这个40Pin管脚中，除了12个电源类外，其余28个都是可编程的GPIO，其中部分GPIO可以复用为IIC，SPI，UART，PWM等等，可以用来驱动各种外设。

I2C是由Philips公司开发的一种简单、双向二线制同步串行总线。它只需要两根线即可在连接于总线上的器件之间传送信息。树莓派通过I2C接口可控制多个传感器和组件。它们的通信是通过SDA(数据引脚)和SCL(时钟速度引脚)来完成的。每个从设备都有一个唯一的地址，允许与许多设备间快速通信。ID_EEPROM引脚也是I2C协议，它用于与HATs通信。

SPI是串行外设接口，用于控制具有主从关系的组件，采用从进主出和主进从出的方式工作，树莓派上SPI由SCLK、MOSI、MISO接口组成，SCLK用于控制数据速度，MOSI将数据从树莓派发送到所连接的设备，而MISO则相反。

有使用Arduino的朋友一定听说过UART或Serial，通用异步收/发器接口用于将Arduino连接到为其编程的计算机上，也用于其他设备与 RX 和 TX 引脚之间的通信。如果树莓派在 raspi-config 中启用了串口终端，则可以使用这些引脚通过电脑来控制树莓派，也可以直接用于控制Arduino。

在树莓派上，所有的引脚都可以实现软件PWM，而GPIO12、GPIO13、GPIO18、GPIO19可以实现硬件脉宽调制。

# mymcu
mcu study &amp; test

### Stm32
- 蓝牙通讯
- OLED
- 温湿度传感器
- 超声波距离传感器

#### Stm32平衡两轮车

### Raspberry PICO
- oled
- bluetooth
- inkPaper with bluetooth
- keybroad_5_4 
  [参考资料1](https://www.instructables.com/Raspberry-Pi-Pico-4x4-Matrix-Keypad-and-1602-LCD-I/)
  [参考资料2](https://how2electronics.com/simple-calculator-using-keypad-oled-raspberry-pi-pico/)
- RYG_led_keybroad_5_4 通过5*4键盘控制红黄绿灯

### Esp32

#### Esp32 cam
- hello
- 视频网络服务器 （Web Video Stream) 
	https://blog.csdn.net/m0_50614038/article/details/130464482
	https://github.com/shariltumin/esp32-cam-micropython-2022
- Arduino 
	arduino-esp32-cam环境配置和例程 https://blog.csdn.net/akk41397/article/details/106419396

### Raspberry Pi
- 设置时间服务器和时区
	+ 安装NTP，输入指令“sudo apt-get install ntpdate ”
	+ 启用NTP，输入指令“sudo timedatectl set-ntp true”
	+ 修改本地时区，输入指令“sudo dpkg-reconfigure tzdata”。
	+ 开机自动设置时区 修改/home/[user]/.profile 增加一行 TZ='Asia/Hong_Kong'; export TZ
- sGate 内网穿透 
  docker run -d --name npc --net=host ffdfgdfg/npc -server=1.94.26.149:8024 -vkey=42apn6r1dps2kmix -type=tcp
- smarGate 内网穿透 
 		适用版本：linux_mini_arm64v0.31.10.tar
 		需安装Openssl: sudo apt install libssl-dev libcurl4 libcurl4-openssl-dev
    后台运行 nohup sudo ./proxy_server -i1000 -o1000 -w8 &
    开机自动运行 添加命令到rc.local文件 exit 0 之前
- 安装Apache2+PHP7.3+Pi Dashboard
	+ 替换国内源
	sudo nano /etc/apt/sources.list 进入编辑界面，删除原有的内容，粘贴如下内容： 
```bash
deb http://mirrors.aliyun.com/raspbian/raspbian/ bullseye main non-free contrib rpi
deb-src http://mirrors.aliyun.com/raspbian/raspbian/ bullseye main non-free contrib rpi
```
	如提示公钥错误，需手动配置公钥：sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9165938D90FDDD2E
	+ 安装软件包（apache2 成功; php 失败）
	安装apache: apt install apache2;systemctl restart apache2.service
- Docker
	[参考教程](https://docker-practice.github.io/zh-cn/install/raspberry-pi.html)
```bash
# 由于 apt 源使用 HTTPS 以确保软件下载过程中不被篡改。因此，我们首先需要添加使用 HTTPS 传输的软件包以及 CA 证书。
sudo apt-get install \
     apt-transport-https \
     ca-certificates \
     curl \
     gnupg2 \
     lsb-release \
     software-properties-common
# 为了确认所下载软件包的合法性，需要添加软件源的 GPG 密钥。
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/raspbian/gpg | sudo apt-key add -
# 官方源
# $ curl -fsSL https://download.docker.com/linux/raspbian/gpg | sudo apt-key add -

# 向 sources.list 中添加 Docker 软件源：
sudo add-apt-repository \
    "deb [arch=armhf] https://mirrors.aliyun.com/docker-ce/linux/raspbian \
    $(lsb_release -cs) \
    stable"

# 官方源
# $ sudo add-apt-repository \
#    "deb [arch=armhf] https://download.docker.com/linux/raspbian \
#    $(lsb_release -cs) \
#    stable"

curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh --mirror Aliyun

# 镜像加速 创建或修改 /etc/docker/daemon.json 文件，修改为如下形式
{
"registry-mirrors": [
    "https://suyxus8r.mirror.aliyuncs.com",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ]
}
# 建立 docker 用户组 并将当前用户加入 docker 组：
$ sudo groupadd docker
$ sudo usermod -aG docker $USER
# 重启服务
sudo systemctl daemon-reload
sudo systemctl restart docker
```
hub.docker.com 查找适配合适内核的镜像 
apache2 + php Docker 多容器运行 PHP-FPM + Apache
https://www.jianshu.com/p/aba42313d79a
```bash
docker pull httpd
docker pull php:7.0.23-fpm
# 修改 Apache 配置文件 
# 打开拷贝到宿主机上的 httpd.conf 文件，找到这三个货色，把前面的#号去掉
LoadModule proxy_module modules/mod_proxy.so
LoadModule proxy_connect_module modules/mod_proxy_connect.so
LoadModule proxy_fcgi_module modules/mod_proxy_fcgi.so
# 注释DocumentRoot "/usr/local/apache2/htdocs" 和 <Directory "/usr/local/apache2/htdocs">...</Directory>
# 增加配置 docker network inspect bridge 查看php-fpm 容器的ip
<VirtualHost *:80>
    ServerAdmin yangke0227@gmail.com
    DocumentRoot "/usr/local/apache2/htdocs"
    ServerName localhost
    <Directory "/usr/local/apache2/htdocs">
     Options None
     Require all granted
    </Directory>
    ProxyRequests Off
    ProxyPassMatch ^/(.*\.php)$ fcgi://172.17.0.2:9000/php/$1
</VirtualHost>
# 启动 PHP-FPM
docker run -itd --name php-fpm -v /opt/php:/php php:7.0.23-fpm
# 启动apache 映射WEB目录和配置文件
docker run -itd -v /opt/php:/usr/local/apache2/htdocs -v /opt/mydocker/php/httpd.conf:/usr/local/apache2/conf/httpd.conf -p 80:80 httpd
```
- Installing InfluxDB & Grafana on Raspberry Pi
	https://simonhearne.com/2020/pi-influx-grafana/	
- Socket
- Gpio
- 中断

### Logs
 - 230717 安装Arduino IDE 配置esp环境
   附加开发板管理器中添加网址：https://dl.espressif.com/dl/package_esp32_index.json
   Arduino开发板选择 Ai Thinker ESP32-CAM
   使用示例CameraWebServer 串流成功 问题：发热较严重；清晰度不够；无录音
 - 230717 闲鱼4B4G(400)   
 - 230818 RaspberryPi OMV SUCCESS
 - 230820 RaspberryPico 超声距离传感器 舵机 控制小垃圾桶开合
 - 230828 光敏电阻 寻轨小车 焊接组装

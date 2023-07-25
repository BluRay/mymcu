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
- smarGate 内网穿透 
 		适用版本：linux_mini_arm64v0.31.10.tar
 		需安装Openssl: sudo apt install libssl-dev libcurl4 libcurl4-openssl-dev
    后台运行 nohup sudo ./proxy_server -i1000 -o1000 -w8 &
    开机自动运行 添加命令到rc.local文件 exit 0 之前
- 安装Apache2+PHP7.3+Pi Dashboard
	+ 替换国内源
	sudo nano /etc/apt/sources.list 进入编辑界面，删除原有的内容，粘贴如下内容： 
```bash
deb http://mirrors.aliyun.com/raspbian/raspbian/ bookworm  main non-free contrib rpi
deb-src http://mirrors.aliyun.com/raspbian/raspbian/ bookworm main non-free contrib rpi
```
	如提示公钥错误，需手动配置公钥：sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv [9165938D90FDDD2E]
	+ 安装软件包（apache2 成功; php 失败）
	安装apache: apt install apache2;systemctl restart apache2.service
	TODO:手动安装和配置PHP5.6
```bash
	tar -zxvf php-5.6.30.tar.gz 
	cd php-5.6.30
	#编译配置
	./configure --prefix=/usr/local/php  --with-curl=/usr/local/curl  --with-freetype-dir  --with-gd  --with-gettext  --with-iconv-dir  --with-kerberos  --with-libdir=lib64  --with-libxml-dir  --with-mysqli  --with-openssl  --with-pcre-regex  --with-pdo-mysql  --with-pdo-sqlite  --with-pear  --with-png-dir  --with-xmlrpc  --with-xsl  --with-zlib  --enable-fpm  --enable-bcmath  --enable-libxml  --enable-inline-optimization  --enable-mbregex  --enable-mbstring  --enable-opcache  --enable-pcntl  --enable-shmop  --enable-soap  --enable-sockets  --enable-sysvsem  --enable-xml  --enable-zip
	#编译安装
	make && make install
	#配置php
	cp php.ini-production /usr/local/php/etc/php.ini 
	#创建php-fpm.conf文件
	cp /usr/local/php/etc/php-fpm.conf.default /usr/local/php/etc/php-fpm.conf
	#配置Apache
	#修改httpd.conf文件，该文件在conf目录下，例如我是j将apache安装在/usr/local/apache下，所以这个文件应该在/usr/local/apache/conf/httpd.conf
	#找到：
	AddType  application/x-compress .Z
	AddType application/x-gzip .gz .tgz
	#添加如下内容
	AddType application/x-httpd-php .php
```
- Socket
- Gpio
- 中断

### Logs
 - 230717 安装Arduino IDE 配置esp环境
   附加开发板管理器中添加网址：https://dl.espressif.com/dl/package_esp32_index.json
   Arduino开发板选择 Ai Thinker ESP32-CAM
   使用示例CameraWebServer 串流成功 问题：发热较严重；清晰度不够；无录音
 - 230717 闲鱼4B4G(400)   
   
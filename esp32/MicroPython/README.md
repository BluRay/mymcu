ESP-WROOM-32:
	刷入MicroPython固件【ESP32_GENERIC-20240222-v1.22.2.bin】
	1.连接硬件: 将 ESP32 开发板通过 USB 线连接到你的电脑。
	2.打开 Thonny IDE:
		2.1进入 工具 (Tools) -> 选项 (Options) -> 解释器 (Interpreter)。
		2.2在 解释器 (Interpreter) 下拉菜单中，选择 MicroPython (ESP32)。
		2.3在 端口 (Port) 下拉菜单中，选择你的 ESP32 所连接的串口（例如 COM3 on Windows, /dev/tty.usbserial-xxxx on macOS/Linux）。如果你不确定是哪一个，可以拔插 USB 线看看哪个选项出现或消失。
		2.4点击 安装或更新固件... (Install or update firmware...)。
		2.5在弹出的窗口中，点击 浏览 (Browse) 选择你刚才下载的 .bin 固件文件。
		2.6确保 端口 (Port) 和 设备 (Device) 正确，然后点击 安装 (Install)。
		2.7等待烧录完成，期间开发板可能会自动重启几次。

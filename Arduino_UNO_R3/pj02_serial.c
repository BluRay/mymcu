/*
 * arduino uno端程序
 * 串口使用情况
 Arduino 	UNO   <------>  Arduino Nano OR Other Driver
					D2    <------>   D6
					D3    <------>   D5
					GND   <------>   GND
 serial -----computer
 serial1----- nano softwearserial
 */
 #include<SoftwareSerial.h>
 SoftwareSerial softSerial(3,2);
 
void setup() {
  //初始化serial，该串口用于与计算机连接通信:
  Serial.begin(9600);
  //初始化serial1，该串口用于与设备B连接通信；
  softSerial.begin(9600);
  softSerial.listen();
}
//两个字符串分别用于存储A,B两端传来的数据
String device_A_String="";
String device_B_String="";
 
void loop() {
  // 读取从计算机传入的数据，并通过softSerial发送个设备B:
  if(Serial.available()>0)
  {
    if(Serial.peek()!='\n')
    {
      device_A_String+=(char)Serial.read();
     
    }
    else
    {
      Serial.read();
      Serial.print("you said:");
      Serial.println(device_A_String);
      softSerial.println(device_A_String);
      device_A_String="";
     
    }
  }
  //读取从设备B传入的数据，并在串口监视器中显示
  if(softSerial.available()>0)
  {
    if(softSerial.peek()!='\n')
    {
      device_B_String+=(char)softSerial.read();
    }
    else
    {
      softSerial.read();
      Serial.print("device B said:");
      Serial.println(device_B_String);
      device_B_String="";
    }
  }
}

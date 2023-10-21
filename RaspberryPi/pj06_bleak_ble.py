# pip3 install bleak
# https://github.com/hbldh/bleak
# https://bleak.readthedocs.io/en/latest/usage.html
# https://juejin.cn/post/7261826051952148540
import asyncio
import sys
from bleak import BleakScanner, BleakClient

# 扫描蓝牙设备
async def discover():
  print('-->Discover Ble Devices Start')
  devices = await BleakScanner.discover()
  for d in devices:
    print(d)
  print('-->Discover Ble Devices End')

# 获取设备Model Number
address = "48:87:2D:64:FA:A8"
MODEL_NBR_UUID = "2A24"
async def getBleModelNumber():
  async with BleakClient(address) as client:
    model_number = await client.read_gatt_char(MODEL_NBR_UUID)
    print("Model Number: {0}".format("".join(map(chr, model_number))))

# 获取设备服务
async def getBleService(address):
  async with BleakClient(address) as client:
    print('-->Client Success')
    services = client.services
    for service in services:
      print("Service UUID:", service.uuid)
      for character in service.characteristices:
        print("uuid:", character.uuid)
        print("properties:", character.properties)
  print("disConnected")
  
    
# 发送数据
# 设备蓝牙地址
# 设备蓝牙UUID
UART_RX_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
UART_TX_CHAR_UUID = "49535343-1E4D-4BD9-BA61-23C647249677"
# 发送数据
data_send = [0x00, 0x11, 0x22]
# 返回数据
data_recive = [0x00, 0x00, 0x00, 0x00, 0x00, 0x0]

async def sent(address, data):
  async with BleakClient(address) as client:
    print(f"Connected: {client.is_connected}")
    await asyncio.sleep(1.0)
    await client.write_gatt_char(UART_RX_CHAR_UUID,bytes(data))
    '''
    paired = await client.pair(protection_level=2)
    print(f"Paired: {paired}")
    while client.is_connected:
      while paired == True:
        print("send data")
        await client.write_gatt_char(UART_RX_CHAR_UUID,bytes(data))
        #await client.start_notify(UART_TX_CHAR_UUID, handle_rx)
        await asyncio.sleep(1.0)
    '''

## START ##
# asyncio.run(discover())
# asyncio.run(getBleModelNumber())
# asyncio.run(sent(address, data_send))
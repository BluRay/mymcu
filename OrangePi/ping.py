# pip install ping3
from ping3 import ping
import time

def ping_forever():
    while True:
        try:
        	response_time = ping('120.24.188.63', timeout=2)
        	if response_time is None:
        		print('Target is unreachable.')
        	else:
        		print(f'Response time: {response_time} seconds')
        except PingError as e:
        	print(f'Ping failed: {e}')
        time.sleep(60)

ping_forever()
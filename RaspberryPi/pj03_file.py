import json
import time

def getFileConf():
  with open('pi.conf', "rt", encoding="utf-8") as file_obj:
    for line in file_obj:
      data = json.loads(line)
      return data['app']

with open('pi.conf', "r+", encoding="utf-8") as file_obj:
  file_obj.read()
  file_obj.write('\n{"app":"mypi2","version":"4b"}')

with open('pi.conf', "rt", encoding="utf-8") as file_obj:
  for line in file_obj:
    data = json.loads(line)
    print(line)
    print(data['app'])
'''    
while 1:
  app = getFileConf()
  print(app)
  time.sleep(5)
 '''
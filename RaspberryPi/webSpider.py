from bs4 import BeautifulSoup

import requests
import urllib.request
import urllib.parse
import re
import time
import urllib.request, urllib.parse, http.cookiejar
from retrying import retry

@retry(stop_max_attempt_number=5, wait_fixed=2000)
def getHtml(url):
	cj = http.cookiejar.CookieJar()
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
	opener.addheaders = [('User-Agent',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'),
	('Cookie', '4564564564564564565646540')]
	urllib.request.install_opener(opener)

	html_bytes = urllib.request.urlopen(url).read()
	html_string = html_bytes.decode('utf-8')
	return html_string

@retry(stop_max_attempt_number=5, wait_fixed=2000)
def savePic(url, filename):
  urllib.request.urlretrieve(url, filename)

def download(file_path, picture_url):
  headers = { "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"}
  r = requests.get(picture_url, headers=headers)
  with open(file_path, 'wb') as f:
    f.write(r.content)

def fileAddLine(str):
  # r+	打开一个文件用于读写。文件指针将会放在文件的开头。
  # a   打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
  # a+	打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
  with open('vspider500.txt', "a", encoding="utf-8") as file_obj:
    #file_obj.read()
    file_obj.write('\n' + str)

if __name__ == '__main__':
  url = "https://missav.com/cn/new?sort=saved&page="
  # Get Cover Start
  for i in range(401, 501):
    curl = url + '%d' % i
    print(curl)
    html_doc = getHtml(curl)
    soup = BeautifulSoup(html_doc,"lxml")
    films = soup.find_all("img", class_="lozad")
    #print(len(films))
    for m in films:
      fileAddLine(m['alt'] + '|' + m['data-src'])
    time.sleep(8)
  # Get Cover Start
  
  # Download Cover Start
  '''
  print('-->start')
  with open('vspider300.txt', 'r', encoding='utf-8') as ff:
    for i in range(0, 901):
      ff.readline()
    for i in range(0, 300):
      str = ff.readline()
      #print(line)
      vname = str[str.find('.com/')+5:str.find('/cover')].upper()
      vtitle = str[:str.find('|')]
      vcover = str[str.find('|')+1:].replace('thumbnail', 'normal').replace('\n','')
      print('%d:' % i + vname + '|' + vcover)
      if (vcover != ''):
        savePic(vcover, 'covers/' + vname + '.jpg')
        #download('1.jpg',vcover)
        time.sleep(5)
  '''
  # Download Cover End


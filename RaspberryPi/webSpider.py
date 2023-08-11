from bs4 import BeautifulSoup

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

def fileAddLine(str):
  # r+	打开一个文件用于读写。文件指针将会放在文件的开头。
  # a   打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
  # a+	打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
  with open('vspider.txt', "a", encoding="utf-8") as file_obj:
    #file_obj.read()
    file_obj.write('\n' + str)

if __name__ == '__main__':
  url = "https://missav.com/cn/new?sort=saved&page="
  for i in range(301, 401):
    curl = url + '%d' % i
    print(curl)
    html_doc = getHtml(curl)
    soup = BeautifulSoup(html_doc,"lxml")
    films = soup.find_all("img", class_="lozad")
	  #print(len(films))
    for m in films:
      fileAddLine(m['alt'] + '|' + m['data-src'])
    time.sleep(8)
		  
	#美丽维纳斯 VIII:https://cdn82.akamai-content-network.com/ipzz-034/cover.jpg?class=thumbnail
	#print(html_doc)
	#urllib.request.urlretrieve(img_url, 't.jpg')
	
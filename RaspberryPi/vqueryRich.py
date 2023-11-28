from rich.console import Console
from rich.table import Table
import sys
import pymysql

def connDb():
  # 打开数据库连接
  db = pymysql.connect(host='127.0.0.1', user='gravity', password='07422770', database='gravity', port=3306)
  return db

def queryDb(db, sql):
  cursor = db.cursor()
  cursor.execute(sql)
  data = cursor.fetchall()
  return data

table = Table(title="Met Movies")
console = Console()
# table.show_lines = True
table.add_column("Req", width=5, justify="right", style="cyan", no_wrap=True)
table.add_column("Code", width=10, style="green")
table.add_column("Cover", width=10, style="green")
table.add_column("Title", width=40, style="magenta")
#table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")

if len(sys.argv) > 1:
  db = connDb()
  print(str(sys.argv[1]))
  sql = "SELECT * FROM tb_fit WHERE vcode LIKE '%%%s%%'" % str(sys.argv[1])
  vinfo = queryDb(db, sql)
  for v in vinfo:
    table.add_row('%d' % v[0], v[1], v[3], v[2])
  
  #print(str(vinfo[0][1:4])[1:len(str(vinfo[0][1:4]))-1])
  console.print(table)
  db.close()
import sys
import pymysql

def connDb():
  # 打开数据库连接
  db = pymysql.connect(host='192.168.1.72', user='root', password='07422770', database='gravity', port=9211)
  # 使用 cursor() 方法创建一个游标对象 cursor
  # cursor = db.cursor()
  return db

def queryDb(db, sql):
  cursor = db.cursor()
  cursor.execute(sql)
  data = cursor.fetchall()
  return data
  
if len(sys.argv) > 1:
  db = connDb()
  print(str(sys.argv[1]))
  sql = "SELECT * FROM tb_fit WHERE vcode LIKE '%%%s%%'" % str(sys.argv[1])
  vinfo = queryDb(db, sql)
  print(vinfo)
  db.close()

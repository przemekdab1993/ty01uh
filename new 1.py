import mysql.connector
import time

dbconfig = { 'host': '127.0.0.1',
			'user': 'root',
			'password': 'root',
			'database': 'flaskserver2018', }

conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor()

_SQL = """SELECT * FROM user"""
cursor.execute(_SQL)
res = cursor.fetchall()


for r in res:
	for i in r:
		print(i)

cursor.close()
conn.close()

time.sleep(10)
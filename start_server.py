from flask import Flask, render_template, request
import mysql.connector
from datetime import datetime

app = Flask(__name__)

dbconfig = { 'host': '127.0.0.1',
			'user': 'root',
			'password': 'root',
			'database': 'flaskserver2018', }

def saveName(req : 'flask_request', res : str, date : 'datetime') -> None:
	with open('log/save.log', 'a') as log:
		print(req, res, date, file = log, sep=" || ")

@app.route('/')
def hello() -> 'html':
	return render_template('home.html', the_title='Home')
	
@app.route('/login')
def log() -> 'html':
	return render_template('login.html', the_title='Login')
	
@app.route('/login_UPP', methods=['POST'])
def login() -> 'html':
	this_date = datetime.today()
	saveName(request.form['user_name'], 'Witaj!!!', this_date)
	return render_template('log_ok.html', the_title = 'Home', the_user_name = request.form['user_name'])
	
@app.route('/viewlog')
def viewsLog() -> str:
	with open('log/save.log') as log:
		const = log.readlines()
		return '////////////////'.join(const)
@app.route('/registration')
def regist() -> 'html':
	return render_template('registration.html', the_title = 'Registration')
		
@app.route('/testBaza')
def test() -> str:
	conn = mysql.connector.connect(**dbconfig)
	cursor = conn.cursor()
	
	_SQL = """INSERT INTO user (user_name, passwd, lvl, experience, silver_coins, gold_coins) VALUES (%s, %s, %s, %s, %s, %s)"""
	cursor.execute(_SQL, ('Jacek', 'placek', '1', '100', '1', '1'))
	conn.commit()
	
	cursor.close()
	conn.close()
	return "ddd"

if __name__ == '__main__':
	app.run(debug = True)

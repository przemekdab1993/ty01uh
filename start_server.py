from flask import Flask, render_template, request, session, json, jsonify
from datetime import datetime
from connectDB import DBco
from random import randint
import time

app = Flask(__name__)

app.secret_key = '0r43ee4y'

""" Dane  logowania do bazy danych """
dbconfig = { 'host': '127.0.0.1',
			'user': 'root',
			'password': 'root',
			'database': 'flaskserver2018', }

def saveName(req : 'flask_request', res : str, date : 'datetime') -> None:
	""" Zapisanie logowania do pliku log """
	with open('log/save.log', 'a') as log:
		print(req, res, date, file = log, sep = " || ")
	
def check_status(func):
	""" SPRAWDZANIE CZY JESTEŚ ZALOGOWANY """
	if 'loged_in' in session:
		return func()
	else:
		return render_template('login.html', the_title='Login', the_log='Login')
		
@app.route('/')
def hello() -> 'html':
	""" STRONA GŁÓWNA """
	if 'loged_in' in session:
		with DBco(dbconfig) as cursor:
			_SQL = """SELECT * FROM (fields_user, content_krotka) WHERE user_ID = (%s) AND fields_user.content_ID = content_krotka.content_ID ORDER BY krotka_ID; """
			cursor.execute(_SQL, (session['user_id'],))
			res = cursor.fetchall()
		return render_template('my_home.html', the_title=res, the_log='Logout', the_src_base=res)
	else:
		return render_template('home.html', the_title='Home', the_log='Login')
	
@app.route('/login')
def log() -> 'html':
	""" STRONA LOGOWANIA """
	def log_out():
		""" Wylogowanie użytkownika """
		session.clear()
		time.sleep(2)
		return render_template('login.html', the_title='Login', the_log='Login')
	return check_status(log_out)
	
@app.route('/login_UPP', methods=['POST'])
def login() -> 'html':
	""" LOGOWANIE """
	user = request.form['user_name']
	passwd = request.form['password']
	
	with DBco(dbconfig) as cursor:
		_SQL1 = """SELECT user_ID FROM user_game WHERE user_name = (%s) AND user_password = (%s) """
		
		cursor.execute(_SQL1, (user, passwd))
		res = cursor.fetchall()
	
	flag = len(res)		
	this_date = datetime.today()
	if flag > 0: 
		""" Poprawne logowanie """
		saveName(request.form['user_name'], 'Witaj!!!', this_date)
		session['loged_in'] = True
		session['user_name'] = user
		session['user_id'] = res[0][0]
		
		return render_template('log_ok.html', the_title = 'Tak', the_log='Logout', the_user_name = request.form['user_name'])
	else:
		""" Jeżeli urzytkownika nie ma w bazie """
		saveName(request.form['user_name'], "Błąd", this_date)
		return render_template('log_ok.html', the_title = 'Nie', the_log='Login', the_user_name = request.form['user_name'])
	
@app.route('/viewlog')
def viewsLog() -> str:
	""" Pokazanie pliku log """
	with open('log/save.log') as log:
		const = log.readlines()
		return '|-#-|'.join(const)
@app.route('/registration')
def regist() -> 'html':
	""" STRONA REJESTRACJI NOWEGO URZYTKOWNIKA """
	return render_template('registration.html', the_title = 'Registration', the_log='Login')
		
@app.route('/adduser', methods=['POST'])
def test() -> str:
	""" REJESTRACJA """
	flag = True
	bed_letter = ['ą', 'ę', 'ó', 'ł', 'ć', 'ż', 'ź', '/', ',', '.', ';', ':']
	user_name = request.form['user_name']
	passwd = request.form['password']
	email =request.form['email']
	
	"""Sprawdzanie user_name """
	if (len(user_name) < 3) or (len(user_name) > 24):
		flag = False
	for i in user_name:
		if i in bed_letter:
			flag = False
	with DBco(dbconfig) as cursor:
		_SQL = """SELECT user_ID FROM user_game WHERE user_name = (%s) """
		cursor.execute(_SQL, (user_name,))
		res = cursor.fetchall()
	res_len = len(res)		
	if res_len > 0:
		flag = False
		
	if flag == True:
		with DBco(dbconfig) as cursor:
			_SQL = """INSERT INTO user_game (user_name, user_password, email, action_punkts, lvl, experience, silver_coins, gold_coins, premium_day) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			cursor.execute(_SQL, (user_name, passwd, email, '15', '1', '0', '1', '1', '7'))
		with DBco(dbconfig) as cursor:
			_SQL1 = """SELECT user_ID FROM user_game WHERE user_name = (%s) and user_password = (%s)"""
			cursor.execute(_SQL1, (user_name, passwd))
			kont = cursor.fetchall()
			user_ID = kont[0][0]
			
			maps = []
			for i in range(81):
				maps.append('1')
			for i in range(20):
				rand = randint(0, 80)
				maps[rand] = '2'
			for i in range(15):
				rand = randint(0, 80)
				maps[rand] = '3'
			for i in range(10):
				rand = randint(0, 80)
				maps[rand] = '4'
			for rote in range(0, 80, 1):
				_SQLX = """INSERT INTO fields_user (user_ID, krotka_ID, content_ID, counter) VALUES (%s, %s, %s, %s);"""
				cursor.execute(_SQLX, (user_ID, rote, maps[rote] , '1'))
		return "succces"
	else:
		return "failed"
@app.route('/items')
def viev_items() -> 'html':
	def views():
		return "Tak jesteś zalogowany"
	
	return check_status(views)

if __name__ == '__main__':
	app.run(debug = True)

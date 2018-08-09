from flask import Flask, render_template, request, session
from datetime import datetime
import jinja2
from connectDB import DBco
import time
import urllib3

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
		return render_template('login.html', the_title=session['next_page'], the_log='Login')
		
@app.route('/')
def hello() -> 'html':
	""" STRONA GŁÓWNA """
	if 'loged_in' in session:
		return render_template('my_home.html', the_title='MY_Home', the_log='Logout')
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
		_SQL1 = """SELECT id FROM user WHERE user_name = (%s) AND passwd = (%s) """
		
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
		return '////////////////'.join(const)
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
	
	"""Sprawdzanie user_name """
	if (len(user_name) < 3) or (len(user_name) > 24):
		flag = False
	for i in user_name:
		if i in bed_letter:
			flag = False
	with DBco(dbconfig) as cursor:
		_SQL = """SELECT id FROM user WHERE user_name = (%s) AND passwd = (%s) """
		
		
		
		
	if flag == True:
		with DBco(dbconfig) as cursor:
			_SQL = """INSERT INTO user (user_name, passwd, lvl, experience, silver_coins, gold_coins) VALUES (%s, %s, %s, %s, %s, %s)"""
			cursor.execute(_SQL, (request.form['user_name'], request.form['password'], '1', '100', '1', '1'))
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

import uuid
import apsw

DB_FILE = "gingo/data/gingo.db"

print 'Creazione nuovo utente'
username = raw_input('username: ')
password = raw_input('password: ')
password2= raw_input('ripetere la password: ')
adm 	 = raw_input('admin? (S/N)')
if adm == 'S':
	is_admin = 1
else:
	is_admin = 0

if password != password2:
	print 'Password NON COINCIDENTI!'
	exit(0)

code = str(uuid.uuid4())

with apsw.Connection(DB_FILE) as db:
	cursor = db.cursor()
	cursor.execute('INSERT INTO USER (username, password, code, is_admin) VALUES (?,?,?,?)', (username, password, code, is_admin))

print 'Creazione utente completata.'

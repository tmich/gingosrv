import os, sys
import time
import apsw
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring

DB_FILE = "gingo/data/gingo.db"

def read_xml_2(xml):
	data = []
	code = ''
	name = ''
	addr = ''
	cap  = ''
	city = ''
	prov = ''
	piva = ''
	tel  = ''
	dtin = ''
	dtum = ''
	
	for event, elem in ET.iterparse(xml, events=('end',)):		
		if elem.tag == 'CLIENTI':
			data.append((code, name, addr, cap, city, prov, piva, tel, dtin, dtum))
		if elem.tag == 'CODCLI':
			code = _t(elem)
		elif elem.tag == 'RAGSOC':
			name= _t(elem)
		elif elem.tag == 'INDIR':
			addr= _t(elem)
		elif elem.tag == 'CAP':
			cap= _t(elem)
		elif elem.tag == 'LOCAL':
			city= _t(elem)
		elif elem.tag == 'PROV':
			prov= _t(elem)
		elif elem.tag == 'PARTIVA':
			piva= _t(elem)
		elif elem.tag == 'TEL':
			tel= _t(elem)
		elif elem.tag == 'DATINS':
			dtin= _t(elem)
		elif elem.tag == 'DATUMOD':
			dtum= _t(elem)

	return data
	
	
def write_to_db(data):
	with apsw.Connection(DB_FILE) as db:
		cursor = db.cursor()
		#if ('(no)', '( no)') not in name:
		cursor.executemany('INSERT OR REPLACE INTO CUSTOMER (code, name, address, cap, city, prov, part_iva, tel, ins_date, mod_date) VALUES (?,?,?,?,?,?,?,?,?,?)', data)


def _t(elem):
	try:
		return unicode(elem.text, 'utf8')
	except TypeError:
		return elem.text
	except Exception as exc:
		print exc
	return ''


def show_progress(i):
	print '\r[{0}] {1}%'.format('#'*(i/10), i)

	
# def db():
	# try:
		# connection=apsw.Connection(DB_FILE)
		# return connection
	# except:
		# print 'Database %s not found. Exiting.' % DB_FILE
	# exit(1)


if __name__ == '__main__':
	start = time.time()
	
	#if not os.path.isfile(DB_FILE):
	#	with apsw.Connection(DB_FILE) as db:
	#	
	#		cursor = db.cursor()
	#		sql= '''CREATE TABLE customer (id INTEGER NOT NULL,code TEXT UNIQUE NOT NULL,name TEXT NOT NULL,address TEXT,part_iva TEXT, tel TEXT
	#				, cap TEXT,city TEXT,prov TEXT,user_id INTEGER,ins_date TEXT, mod_date TEXT, PRIMARY KEY (id));'''
	#		
	#		cursor.execute(sql)

	data = read_xml_2('clienti.xml')
	print time.time()-start, 'seconds; xml parsed, writing to db'
	write_to_db(data)
	print 'Completed in ', time.time()-start, 'seconds.'

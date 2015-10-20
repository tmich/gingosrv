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
	pric = 0.00
	dtin = ''
	dtum = ''
	
	for event, elem in ET.iterparse(xml, events=('end',)):		
		if elem.tag == 'ARTICOL':
			data.append((code, name, pric))
		if elem.tag == 'CODART':
			code = _t(elem)
		elif elem.tag == 'DESART':
			name = _t(elem)
		elif elem.tag == 'PREZZO1':
			pric = _d(elem)
		#elif elem.tag == 'DATINS':
		#	dtin = _t(elem)
		#elif elem.tag == 'DATUMOD':
		#	dtum= _t(elem)

	return data
	
	
def write_to_db(data):
	with apsw.Connection(DB_FILE) as db:
		cursor = db.cursor()
		cursor.executemany('INSERT OR REPLACE INTO PRODUCT (code, name, price) VALUES (?,?,?)', data)

def _t(elem):
	try:
		return unicode(elem.text, 'utf8')
	except TypeError:
		return elem.text
	except Exception as exc:
		print exc
	return ''

def _d(elem):
	try:
		text = elem.text.replace(',','.')
		return float(text)
	except Exception as exc:
		print exc
	return 0.00

if __name__ == '__main__':
	start = time.time()
	
	data = read_xml_2('articoli.xml')
	print time.time()-start, 'seconds; xml parsed, writing to db'
	write_to_db(data)
	print 'Completed in ', time.time()-start, 'seconds.'

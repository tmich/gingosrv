import os
import apsw
import xml.etree.ElementTree as ET

DB_FILE = "test.db"

def read_xml(xml):
		tree = ET.parse(xml)
		root = tree.getroot()

		for cliente in root.findall('CLIENTI'):
			code = get_text(cliente, 'CODCLI')
			name = get_text(cliente, 'RAGSOC')
			addr = get_text(cliente, 'INDIR')
			cap  = get_text(cliente, 'CAP')
			city = get_text(cliente, 'LOCAL')
			prov = get_text(cliente, 'PROV')
			piva = get_text(cliente, 'PARTIVA')
			tel  = get_text(cliente, 'TEL')
			dtin = get_text(cliente, 'DATINS')
			dtmd = get_text(cliente, 'DATUMOD')

			tup  = (code, name, addr, cap, city, prov, piva, tel, dtin, dtmd)
			print tup

def read_xml_2(db, xml):
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
	
	
	for event, elem in ET.iterparse(xml, events=('start', 'end')):
		if elem.tag == 'CLIENTI':
			if event == 'start':
				pass
				#cliente = {}
				# print '**** new cliente'
			elif event == 'end':
				sql = 'INSERT OR REPLACE INTO CUSTOMER (code, name, address, cap, city, prov, part_iva, tel, ins_date, mod_date) VALUES (?,?,?,?,?,?,?,?,?,?)'
				cursor.execute(sql, (code, name, addr, cap, city, prov, piva, tel, dtin, dtum))
				# print '** CREATED **'
				
		if event == 'end':
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
				
def _t(elem):
	try:
		return elem.text
	except:
		print elem.tag + ' not a text node'
		return ''

def db():
        if os.path.isfile(DB_FILE):
                os.remove(DB_FILE)
        connection=apsw.Connection(DB_FILE)
        return connection

if __name__ == '__main__':
	with db() as db:
		cursor = db.cursor()
		#cursor.execute("create table product(id integer primary key, code text, name text, price float)")
		sql= '''CREATE TABLE customer (id INTEGER NOT NULL,code TEXT UNIQUE NOT NULL,name TEXT NOT NULL,address TEXT,part_iva TEXT, tel TEXT
			    , cap TEXT,city TEXT,prov TEXT,user_id INTEGER,ins_date TEXT, mod_date TEXT, PRIMARY KEY (id));'''
		cursor.execute(sql)

		read_xml_2(db, 'clienti.xml')
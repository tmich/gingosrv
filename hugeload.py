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

def read_xml_2(xml):
	results = []
	
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
	cliente = {}
	
	for event, elem in ET.iterparse(xml, events=('start', 'end')):
		# data = (code, name, addr, cap, city, prov, piva, tel, dtin, dtum)
		if elem.tag == 'CLIENTI':
			if event == 'start':
				cliente = {}
				# print '**** new cliente'
			elif event == 'end':
				# print cliente
				results.append(cliente)
		
		if event == 'end':
			if elem.tag == 'CODCLI':
				cliente['code'] = _t(elem)
			elif elem.tag == 'RAGSOC':
				cliente['name'] = _t(elem)
			elif elem.tag == 'INDIR':
				cliente['addr'] = _t(elem)
			elif elem.tag == 'CAP':
				cliente['cap'] = _t(elem)
			elif elem.tag == 'LOCAL':
				cliente['city'] = _t(elem)
			elif elem.tag == 'PROV':
				cliente['prov'] = _t(elem)
			elif elem.tag == 'PARTIVA':
				cliente['piva'] = _t(elem)
			elif elem.tag == 'TEL':
				cliente['tel'] = _t(elem)
			elif elem.tag == 'DATINS':
				cliente['dtin'] = _t(elem)
			elif elem.tag == 'DATUMOD':
				cliente['dtum'] = _t(elem)
	
	print len(results)
				
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
        read_xml_2('clienti.xml')

        #connection = db()
        #cursor = connection.cursor()
        #cursor.execute("create table product(id integer primary key, code text, name text, price float)")

        #connection.close(True)

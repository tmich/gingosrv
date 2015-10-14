from gingo import app
from gingo.data.models import db, User #, Customer, Product

with app.app_context():
	db.drop_all()
	db.create_all()

	adm=User('admin', 'admin', True)
	tiz=User('tiziano', 'tiziano', False)
	# c=Customer('NAPPA', 'Bar Nappa srl', u)
	# p1=Product('P0001', 'cornetti prelievit. Lizzi 1kg', 10.00)
	# p2=Product('P0002', 'fragole senga sengana 1kg', 8.00)

	db.session.add(adm)
	db.session.add(tiz)
	# db.session.add(c)
	# db.session.add(p1)
	# db.session.add(p2)
	
	db.session.commit()
	
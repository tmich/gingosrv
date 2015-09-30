# models
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from hashlib import md5

db = SQLAlchemy()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(32))

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def __repr__(self):
		return '<User %r>' % self.username

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(10))
	name = db.Column(db.String(80))
	price = db.Column(db.Float)
	
	def __init__(self, code=None, name=None, price=0.00):
		self.code = code
		self.name = name
		self.price = price
	
	def __repr__(self):
		return '<Product %r>' % self.name
		
	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'id'	: self.id,
			'code'	: self.code,
			'name'	: self.name,
			'price'	: self.price,
			'hash'	: self.hash
		}
	
	@property
	def hash(self):
		return md5('{0}{1}'.format(self.name, self.price if self.price != None else 0.00).encode()).hexdigest()

class Customer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.Text)
	name = db.Column(db.Text)
	address = db.Column(db.Text)
	part_iva = db.Column(db.Text)
	cap = db.Column(db.Text)
	city = db.Column(db.Text)
	prov = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	user = db.relationship('User',
		backref=db.backref('customer', lazy='dynamic'))
	
	def __init__(self, code=None, name=None, user=None):
		self.code = code
		self.name = name
		self.user = user
	
	def __repr__(self):
		return '<Customer %r>' % self.name
	
	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'id'		: self.id,
			'code'		: self.code,
			'name'		: self.name,
			'address'	: self.address,
			'iva'		: self.part_iva,
			'cap'		: self.cap,
			'city'		: self.city,
			'prov'		: self.prov,
			'tel'		: ''
		}
		
	@property
	def hash(self):
		return md5('{0}{1}'.format(self.name, self.address if self.address != None else "" + self.city if self.city != None else "" + self.part_iva if self.part_iva != None else "" + self.cap if self.cap != None else "").encode()).hexdigest()

class Purchase(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
	creation_date = db.Column(db.DateTime)
	
	user = db.relationship('User',
		backref=db.backref('purchases', lazy='dynamic'))
	
	customer = db.relationship('Customer',
		backref=db.backref('purchases', lazy='dynamic'))
	
	def __init__(self, user, customer):
		self.user = user
		self.customer = customer
		self.creation_date = datetime.utcnow()
	
	def __repr__(self):
		return '<Purchase %r>' % self.id

class PurchaseItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
	purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'))
	qty = db.Column(db.Integer)
	notes = db.Column(db.Text)
	discount = db.Column(db.Text)
	
	product = db.relationship('Product')
	purchase = db.relationship('Purchase',
		backref=db.backref('items', lazy='dynamic'))
	
	def __init__(self, qty, product, notes=None, discount=None):
		#self.purchase = purchase
		self.qty = qty
		self.product = product
		self.notes = notes
		self.discount = discount

	def __repr__(self):
		return '<PurchaseItem %r %r>' % (self.qty, self.product.name)
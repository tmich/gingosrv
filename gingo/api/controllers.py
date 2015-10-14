# ----------------
# api calls (v1.0)
# ----------------
from flask import Blueprint, render_template, request, abort
from flask.json import jsonify
from gingo.data.models import *
from datetime import datetime

## BASE_PATH = '/api/v1.0'

api = Blueprint('api', __name__, template_folder='templates')

@api.route('/')
def hello_world():
	return 'Hello World!'
	
@api.route('/login', methods=['POST'])
def login():
	# do the login
	username = request.json['username']
	password = request.json['password']
	
	print "richiesto login, username %s, password %s" % (username, password)
	
	if username and password:
		user = User.query.filter(User.username == username).filter(User.is_admin == False).first()
		if user:
			if user.password == password:
				return jsonify({"code" : user.code, 'username' : username})
	abort(401)

@api.route('/products', methods=['GET'])
def get_products():
	#print("Found {0} products.".format(len(Product.query.all())))
	return jsonify(json_list=[i.serialize for i in Product.query.all()])

@api.route('/customers/', methods=['GET'])
def get_customers():
	#print("Found {0} customers.".format(len(Customer.query.all())))
	return jsonify(json_list=[i.serialize for i in Customer.query.all()])
	
@api.route('/orders/new', methods=['POST'])
def new_order():
	user_id = request.json['user_id']
	customer_code = request.json['customer_code']
	type = request.json['type']
	
	if type == "I":
		abort(500)
		
	purchase = Purchase(User.query.get(user_id), Customer.query.filter(Customer.code == customer_code).first())
	db.session.add(purchase)
	
	for i in request.json['items']:
		item = PurchaseItem(qty=i['qty'], product=Product.query.filter(Product.code == i['product_code']).first(), notes=i['notes'])
		item.purchase = purchase
		db.session.add(item)
	
	db.session.commit()
	
	print("Ricevuto ordine con {0} prodotti:".format(purchase.items.count()))
	print("Cliente: " + Customer.query.filter(Customer.code == customer_code).first().name)
	print("Data creazione: " + purchase.creation_date.strftime('%d-%m-%Y %H:%M:%S'))
	for item in purchase.items:
		print("%rx %r [%r]" % (item.qty, item.product.name, item.notes))
	
	return jsonify({"id" : purchase.id})
	
@api.route('/icewer/new', methods=['POST'])
def new_order_icewer():
	user_id = request.json['user_id']
	customer_code = request.json['customer_code']
	type = request.json['type']
	
	if type != "I":
		abort(500)
	
	purchase = IcewerPurchase(User.query.get(user_id), Customer.query.filter(Customer.code == customer_code).first())
	db.session.add(purchase)
	
	for i in request.json['items']:
		item = IcewerPurchaseItem(qty=i['qty'], product_code=['product_code'], notes=i['notes'])
		item.purchase = purchase
		db.session.add(item)
	
	db.session.commit()
	
	print("Ricevuto ordine ICE-WER con {0} prodotti:".format(o.items.count()))
	print("Cliente: " + Customer.query.filter(Customer.code == customer_code).first().name)
	print("Data creazione: " + o.creation_date.strftime('%d-%m-%Y %H:%M:%S'))
	for item in o.items:
		print("%rx %r [%r]" % (item.qty, item.product_code, item.notes))
	
	return jsonify({"id" : o.id})
	
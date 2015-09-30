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
	username = request.form.get('username')
	password = request.form.get('password')
	
	if username and password:
		user = User.query.filter_by(username=username).first()
		#print("ricerca utente %s, %s" % (username, password))
		if user:
			#print("utente {0} trovato".format(username))
			if user.password == password:
				#session['user_id'] = user.id
				return jsonify({"id" : user.id, 'username' : username})
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
	customer_id = request.json['customer_id']
	o = Purchase(User.query.get(user_id), Customer.query.get(customer_id))
	db.session.add(o)
	
	for i in request.json['items']:
		item = PurchaseItem(qty=i['qty'], product=Product.query.get(int(i['product_id'])), notes=i['notes'])
		o.items.append(item)
		db.session.add(item)
	
	db.session.commit()
	
	print("Ricevuto ordine con {0} prodotti".format(o.items.count()))
	print(o.creation_date.strftime('%d-%m-%Y %H:%M:%S'))
	
	return jsonify({"id" : o.id})
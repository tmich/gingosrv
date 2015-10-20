import json
from gingo import app
from gingo.data.models import Customer, Product

print("Generating static data...")
with app.app_context():
	cs = json.dumps([i.serialize for i in Customer.query.all()], separators=(',',':'))
	ps = json.dumps([i.serialize for i in Product.query.all()], separators=(',',':'))

	print("Writing data to .json files")

	with open("customers.json", "w") as out1:
		out1.write(cs)

	with open("products.json", "w") as out2:
		out2.write(ps)

	print("Done")

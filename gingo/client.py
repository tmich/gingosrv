#import json
import urllib.request

details = urllib.parse.urlencode({ 'username': 'nappa', 'password': 'lallo' }).encode('UTF-8')

with urllib.request.urlopen("http://128.128.1.85:5000/api/v1.0/login", details) as response:
	json = response.read().decode('utf8', 'ignore')

print(json)
from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017/')
db = client.gmaps
collection = db.gmaps
# posts = db.posts
posts = db.health

def list_all_places():
	return db.health.find({'type': 'place'})


def listAllPlaces():
	lista = list_all_places()
	places = {}
	for i in lista:
		name = i['region'].replace('Sao Jose Dos Campos','') + ' - ' + i['neighborhood']
		if name not in places:
			places[name] = [0.0, 0]
		places[name][0] += i['price']
		places[name][1] += i['square_meter']

	for i in places:
		places[i].append(places[i][0] / places[i][1])

	result = []
	for i in sorted(places.keys()):
		f = "{:.2f}".format(places[i][2])
		print(i, f)


# listAllPlaces()
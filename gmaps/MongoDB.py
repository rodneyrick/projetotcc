from pymongo import MongoClient
import datetime
import json

client = MongoClient('mongodb://localhost:27017/')
db = client.gmaps
collection = db.gmaps
posts = db.health

def list_all_macro_regions():
	l = []
	for i in db.health.find({'type' : 'macro_region'}):
		l.append(i)
	return l

def list_all_healths():
	l = []
	for i in db.health.find({'type' : 'Hospital'}):
		l.append([ i['type'] + ' - ' + i['name'], i['lat'], i['lng'], i['color']])
	for i in db.health.find({'type' : 'UPA'}):
		l.append([ i['type'] + ' - ' + i['name'], i['lat'], i['lng'], i['color']])
	for i in db.health.find({'type' : 'UBS'}):
		l.append([ i['type'] + ' - ' + i['name'], i['lat'], i['lng'], i['color']])
	return l

def list_all_healths_2_table():
	l = []
	for i in db.health.find({'type' : 'Hospital'}).sort('region', 1):
		l.append(i)
	for i in db.health.find({'type' : 'UPA'}).sort('region', 1):
		l.append(i)
	for i in db.health.find({'type' : 'UBS'}).sort('region', 1):
		l.append(i)
	return l

def list_all_postal_codes():
	l = []
	for i in db.health.find({'type' : 'postal_code'}):
		l.append(i)
	return l

def list_all_cids_groups():
	l = {}
	for i in db.health.find({'type' : 'cid'}).sort('neoplasms_group',1):
		l[i['neoplasms_group']] = i['neoplasms_group_description']
	return json.loads(json.dumps(l,sort_keys=True))

def insert_postal_code(d):
	p = db.health.find({ 'type': 'postal_code', 'postal_code': d['postal_code']})
	if p is None:
		db.health.insert(d)
	return d

def find_postal_code(pc):
	return db.health.find_one({ 'type': 'postal_code', 'postal_code': pc})

def find_city(city):
	return db.health.find_one({ 'type': 'city', 'locality': city})

def insert_item(d):
	try:
		db.health.insert(d)
	except Exception as e:
		pass

def list_all_cids():
	p = db.health.find({'type': 'cid'}).sort('code', 1)
	l = []
	for i in p:
		l.append(i)
	return l

def list_all_cids2():
	return db.health.find({'type': 'cid'}).sort('code', 1)

def list_all_documents():
	p = db.health.find({'type': 'file'}).sort('date', -1).limit(50)
	l = []
	for i in p:
		l.append(i)
	return l

def remove_all_documents():
	db.health.remove( { 'type' : 'file' } )

def list_all_places():
	return db.health.find({'type': 'place'})

def list_all_regions():
	return db.health.find({'type': 'region'})


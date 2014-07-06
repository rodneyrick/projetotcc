# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import string
import sys
import json
import unicodedata
import MongoDB

def generateCeps(maxx, firstPart, secondPart):
	"""
	Returns the maximum amount of desired ceps without repetition
	maxx -> amount
	firstPart -> list of init cep [init, final]
	secondPart -> list of second part of cep [init, final]
	"""
	import random
	lista = []
	ceps = ''
	for i in range(maxx):
		r = '{0}-{1:03d}'.format(random.randint(firstPart[0], firstPart[1]), 
			random.randint(secondPart[0], secondPart[1]))
		if r not in lista:
			lista.append(r)
	return lista

list_postal_codes = []
def geocode2(cep, isCenter=False, **geo_args):
	GEOCODE_BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json'
	url = GEOCODE_BASE_URL + '?' + urllib.parse.urlencode(geo_args)
	req = urllib.request.urlopen(url)
	data = req.read()
	result = json.loads(data.decode("utf-8"))
	try:
		d = {}
		for i in result['results'][0]['address_components']:
			if 'route' in i['types']:
				d['address'] = i['long_name']

			elif 'neighborhood' in i['types']:
				d['neighborhood'] = i['long_name']

			elif 'locality' in i['types']:
				d['locality'] = i['long_name']

			elif 'administrative_area_level_1' in i['types']:
				d['abbreviation_state'] = i['short_name']
				d['state'] = i['short_name']

			elif 'country' in i['types']:
				d['abbreviation_country'] = i['short_name']
				d['country'] = i['long_name']

		if isCenter:
			d['type'] = 'city'
		else:
			d['type'] = 'postal_code'
			d['postal_code'] = cep
		d['lat'] = result['results'][0]['geometry']['location']['lat']
		d['lng'] = result['results'][0]['geometry']['location']['lng']
		return d
	except IndexError as e:
		# print("PAU", cep) #, result)
		global list_postal_codes
		list_postal_codes.append(geo_args['address'])

def geocode(address, isCenter=False, sensor="false", **geo_args):
	cep = ''
	if isCenter:
		pc = MongoDB.find_city(address[1])
		if pc is None:
			geo_args.update({
				'address': address[0].replace(' ', '+'),
				'sensor': sensor
			})
			# print(address)
			temp = geocode2(address[0], isCenter=True, **geo_args)
			MongoDB.insert_item(temp)
			return temp
		else:
			return pc
	else:
		cep = address[1]
		pc = MongoDB.find_postal_code(cep)
		if pc is None:
			geo_args.update({
				'address': address[0].replace(' ', '+'),
				'sensor': sensor
			})
			temp = geocode2(cep, **geo_args)
			MongoDB.insert_item(temp)
			return temp
		else:
			return pc


WORKERS = 1
def parallelGeocode(ceps_list):
	import concurrent.futures as future
	# import time
	def waiter(executor, cep):
		# time.sleep(0.01)
		return executor.submit(geocode, cep)
	result = None
	with future.ThreadPoolExecutor(max_workers=WORKERS) as executor:
		result = [waiter(executor, cep) for cep in ceps_list]
	l = [computation.result() for computation in future.as_completed(result) if computation.result() is not None]
	while list_postal_codes:
		p = list_postal_codes.pop()
		l.append(geocode(p))
	return l

# p = generateCeps(50000, [12200, 12248], [1,999])

# for i in p:
# 	d = geocode('Brasil SP São José dos Campos ' + i, isCenter=False )
# 	print(d)
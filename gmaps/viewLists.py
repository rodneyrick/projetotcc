# -*- coding: utf-8 -*-
import datetime
import time
import MongoDB
import random
import re
import ColorsRandom
import math
import numpy

from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
	"""
	Calculate the great circle distance between two points 
	on the earth (specified in decimal degrees)
	"""
	# convert decimal degrees to radians 
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

	# haversine formula 
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a)) 

	# 6367 km is the radius of the Earth
	km = 6367 * c
	return km 

def listAllMacroRegions():
	"""
	Retorna todas as micro-regiões consolidadas
	function() -> list
	"""
	lista = MongoDB.list_all_macro_regions()
	return lista

def getDataMacroRegion():
	"""
	Retorna um dictionary com todas as micro-regioes
	function() -> dictionary
	"""
	# from scipy.spatial.distance import euclidean
	dic = {}
	lista = MongoDB.list_all_macro_regions()

	for i in lista:
		d = {}
		if i['region'] not in dic:
			dic[i['region']] = {}
		for j in lista:
			if i['region'] != j['region']:
				# d[j['region']] = float("{0:.4f}".format(euclidean( [i['lng'], i['lat']],  [ j['lng'], j['lat'] ])))
				d[j['region']] = float("{0:.3f}".format(haversine(i['lng'], i['lat'], j['lng'], j['lat'] )))
		dic[i['region']] = d
	lista = MongoDB.list_all_macro_regions()
	for i in lista:
		dic[i['region']]['Price/m²'] = float("{0:.2f}".format(i['price_by_meter']))
		dic[i['region']]['Residents'] = int(i['residents'])
		dic[i['region']]['Occupied Private Housing'] = int(i['occupied_private_housing'])
		dic[i['region']]['Residents Per Household'] = float("{0:.2f}".format(i['residents_per_household']))
		dic[i['region']]['Hospital'] = int(i['hospital'])
		dic[i['region']]['UBS'] = int(i['ubs'])
		dic[i['region']]['UPA'] = int(i['upa'])
		dic[i['region']]['University'] = int(i['university'])
		dic[i['region']]['Bank'] = int(i['bank'])
		dic[i['region']]['Shopping'] = int(i['shopping'])
		dic[i['region']]['Delegacy'] = int(i['delegacy'])
		dic[i['region']]['Market'] = int(i['market'])
		dic[i['region']]['School'] = int(i['school'])
	return dict(sorted(dic.items()))


def randomCIDs(quantity=0):
	"""
	Cria uma quantidade aleatória de CIDs para utilizar e	
	Retorna um dictionary com todas os CIDs gerados, 
	uma lista com cada CIDs, com suas cores devidas, e 
	um dictionary com as cores para cada CID
	function(number) -> dictionary, list, dictionary
	"""
	from collections import Counter
	lista = MongoDB.list_all_cids()
	colors = ColorsRandom.parallel_gen_colors(quantity)
	randomList = []
	while len(randomList) < quantity:
		item = random.choice(lista)
		randomList.append(item['code'])

	dic = dict(Counter(randomList))

	colors = ColorsRandom.parallel_gen_colors(len(dic))

	dicColors = {}
	count = 0
	for i in dic:
		dicColors[i] = colors[count]
		count+=1

	latLng = []
	lista = MongoDB.list_all_postal_codes()
	while len(latLng) < quantity:
		cid = randomList.pop()
		item = random.choice(lista)
		latLng.append(
			[cid, item['lat'], item['lng'], dicColors[cid] ]
		)

	return dic, latLng, dicColors


def listAllDocuments():
	"""
	Retorna uma lista com todos os documentos do sistema, ordenados pela data
	function() -> list
	"""
	lista = MongoDB.list_all_documents()
	docs = [
		[ i['name'], i['extension'], datetime.datetime.fromtimestamp(i['date'])]
		for i in lista
	]
	return docs

def listAllCIDs():
	"""
	Retorna uma lista com todos os documentos do sistema, ordenados pela data
	function() -> list
	"""
	lista = MongoDB.list_all_cids()
	cids = [
		[ i['code'], i['neoplasms'] ]
		for i in lista
	]
	return cids

def listAllHealths():
	"""
	Retorna uma lista com todos os pontos de saude, com a COR, NOME e ENDERECO
	function() -> list
	"""
	lista = MongoDB.list_all_healths_2_table()
	hospitals = [
		[ i['region'], i['name'], i['address'], i['color'] ]
		for i in lista if i['type'] == 'Hospital'
	]
	upas = [
		[ i['region'], i['name'], i['address'], i['color'] ]
		for i in lista if i['type'] == 'UPA'
	]
	ubs = [
		[ i['region'], i['name'], i['address'], i['color'] ]
		for i in lista if i['type'] == 'UBS'
	]
	return hospitals, upas, ubs

def listAllPlaces():
	"""
	Retorna uma lista com todos os lugares, com o preco/m2
	function() -> list
	"""
	lista = MongoDB.list_all_places()
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
		result.append([i, f])
	return result

def excel():
	"""
	Faz um print para poder verificar todos os pontos consolidados
	function()
	"""
	l = MongoDB.list_all_places()
	places = {}
	for i in l:
		name = i['region'].replace('Sao Jose Dos Campos','') + ' - ' + i['neighborhood']
		if name not in places:
			places[name] = ['', '', 0.0, 0]
		places[name][0] = i['region'].replace('Sao Jose Dos Campos','')
		places[name][1] = i['neighborhood']
		places[name][2] += i['price']
		places[name][3] += i['square_meter']
	
	for i in places:
		places[i].append(places[i][2] / places[i][3])

	for i in places:
		print( '{0}\t{1}\t{2}'.format (places[i][0], places[i][1], str(places[i][4])))

def listAllNeighborhood():
	"""
	Print para verificação dos dados
	places[name][0]['abbreviation_state'] = i['abbreviation_state']
	places[name][1]['abbreviation_currency'] = i['abbreviation_currency']
	places[name][2]['region'] = i['region']
	places[name][3]['currency'] = i['currency']
	places[name][4]['state'] = i['state']
	places[name][5]['type'] = i['type']
	places[name][6]['locality'] = i['locality']
	places[name][7]['country'] = i['country']
	places[name][8]['abbreviation_country'] = i['abbreviation_country']
	places[name][9]['neighborhood'] = i['neighborhood']
	places[name][10]['price'] = 0
	places[name][11]['square_meter'] = 0
	places[name][12]['price_by_meter'] = 0
	"""
	lista = MongoDB.list_all_places()
	places = {}
	for i in lista:
		name = i['region'].replace('Sao Jose Dos Campos','') + ' - ' + i['neighborhood']
		if name not in places:
			places[name] = ['','','','','','','','','','',0,0,0]
			places[name][0] = i['abbreviation_state']
			places[name][1] = i['abbreviation_currency']
			places[name][2] = i['region']
			places[name][3] = i['currency']
			places[name][4] = i['state']
			places[name][5] = i['type']
			places[name][6] = i['locality']
			places[name][7] = i['country']
			places[name][8] = i['abbreviation_country']
			places[name][9] = i['neighborhood']
			places[name][10] = 0
			places[name][11] = 0
			places[name][12] = 0
		
		places[name][10] += i['price']
		places[name][11] += i['square_meter']


	for i in places:
		places[i][12] = (places[i][10] / places[i][11])

	print(places)

def r2(newY, listY):
	"""
	Cálculo da qualidade de R2.
	Retorno dos valores:
		1 - R2
		2 - SQr (Soma dos Quadrados dos Residuos)
		3 - SQt (Soma Total dos Quadrados)
	entrance --> list, array
	return --> float, float, float
	"""
	# Soma dos Quadrados dos Residuos
	sqr=0
	for a,b in zip(newY,listY):
		temp = math.pow(a - b[0], 2)
		sqr += temp
	
	# Soma Total dos Quadrados
	sqt=0
	mean = numpy.mean(newY)
	for a in listY:
		temp = math.pow(a[0] - mean, 2)
		sqt+=temp

	# print('SQr', sqr)
	# print('SQt', sqt)
	rAjustado = 1.0 - (sqt/sqr)
	rAjustado = float("{0:.3f}".format(rAjustado))
	return rAjustado, sqr, sqt

def listTableMoreInputs():
	"""
	Retorna a tabela com dos dados que serão escolhidos para compor a sulção de analise regressiva
	function() -> list, matrix (list of lists)
	"""
	l = MongoDB.list_all_macro_regions()
	regions = {}
	for i in l:
		if i['region'] not in regions:
			regions[i['region']] = {}
		for k,v in sorted(i.items()):
			if k not in [ '_id', 'lat', 'lng', 'qtd', 'type', 'region']:
				regions[i['region']][k] = v

	regionsList = []
	isFirstLine = True
	matrix = {}
	for r, values in sorted(regions.items()):
		regionsList.append(r)
		for k,v in sorted(values.items()):
			if k not in matrix:
				matrix[k] = []
			if k == 'price_by_meter':
				matrix[k].append(float("{0:.2f}".format(v)))
			else:
				matrix[k].append(v)
	return regionsList, matrix

def json2matrix(json, fieldY='price_by_meter'):
	"""
	Retorna 
		cabecalho --> list
		result --> matrix
		expression --> HTML
		rAjustado --> number
		sqr (Soma dos Quadrados dos Residuos) --> number
		sqt (Soma Total dos Quadrados) --> number
		table --> HTML
	function(JSON, string) -> list, list, string, number, number, HTML
	"""
	cabecalho = []
	A = []
	for i in json:
		l = []
		for j in i:
			if j == 'field' and i[j] not in cabecalho:
				cabecalho.append(i[j])
			else:
				if( '.' in i[j]):
					l.append(float(i[j]))
				else:
					l.append(int(i[j]))
		A.append(l)

	listY = [[i] for i in A[cabecalho.index(fieldY)]]
	listFields = [ i['field'] for i in json]

	from numpy import matrix
	Amatrix = matrix(A).T
	result = (Amatrix.T * Amatrix)
	result = result.I * Amatrix.T
	result = result * matrix(listY)

	newY = []
	for line in range(0,Amatrix.shape[0]):
		y = 0.0
		for col in range(0,Amatrix.shape[1]):
			y += result.item(col) * Amatrix.item((line, col))
		newY.append(y)

	dicY = ['centro','leste','norte','oeste','sudeste','sul']

	reg=0
	tableY = '''<table class="table"><thead><tr><th>Region</th><th>Y</th><th>new Y</th><th>Difference</th></tr></thead><tbody>'''
	for i in dicY:
		tableY += '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>'.format(dicY[reg], listY[reg][0], newY[reg], float(listY[reg][0] - newY[reg]))
		reg+=1
	tableY += '</tbody></table>'

	rAjustado, sqr, sqt = r2(newY, listY)

	expression = ''
	count=0
	table = '<table class="table"><thead><tr><th>Variable</th><th>Description</th></tr></thead><tbody>'
	listFields
	for i in result:
		p = float(i.item(0))
		expression += '{0}*x<sub>{1}</sub> +<br><br>'.format(str(p), str(count))
		if listFields[count] == fieldY:
			table += '<tr><td>y</td><td>{1}</td></tr>'.format(str(count), listFields[count])
		else:
			table += '<tr><td>x<sub>{0}</sub></td><td>{1}</td></tr>'.format(str(count), listFields[count])
			count+=1
	expression = expression[:-11]
	table += '</tbody></table>'


	return tableY, result, expression, rAjustado, sqr, sqt, table




json = [{"field":"university","centro":"4","leste":"0","norte":"1","oeste":"2","sudeste":"0","sul":"3"},{"field":"occupied_private_housing","centro":"16687","leste":"36229","norte":"14743","oeste":"11813","sudeste":"8592","sul":"48927"},{"field":"shopping","centro":"1","leste":"0","norte":"0","oeste":"0","sudeste":"0","sul":"1"},{"field":"hospital","centro":"1","leste":"1","norte":"1","oeste":"0","sudeste":"0","sul":"1"},{"field":"residents","centro":"49643","leste":"125809","norte":"50073","oeste":"35326","sudeste":"30464","sul":"163862"},{"field":"price_by_meter","centro":"4604.61","leste":"3244.03","norte":"3066.76","oeste":"5324.67","sudeste":"2833.41","sul":"3730.59"}]


print(json2matrix(json))
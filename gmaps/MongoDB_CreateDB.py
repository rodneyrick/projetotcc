from pymongo import MongoClient
import datetime
import json

client = MongoClient('mongodb://localhost:27017/')
db = client.gmaps
collection = db.gmaps
health = db.health

def createDataBase():
	lista = [
		{"type" : "Hospital", "region": "Central", "name":"Hospital Dia", "address": "Rua Amin Assad, 200, São Dimas", "lat" : -23.2009319, "lng" : -45.8878566 , "color" : "#CC9966"},
		{"type" : "Hospital", "region": "Leste", "name":"Hospital Municipal", "address": "Rua Saigiro Nakamura, 800, Vila Industrial", "lat" : -23.1798667, "lng" : -45.8545143 , "color" : "#383838"},
		{"type" : "Hospital", "region": "Norte", "name":"Hospital de Clínicas Norte", "address": "Rua Alziro Lebrão 76, bairro Alto da Ponte", "lat" : -23.153673, "lng" : -45.901411 , "color" : "#CC9966"},
		{"type" : "Hospital", "region": "Sul", "name":"Hospital de Clínicas Sul", "address": "Praça Natal, 55, Parque Industrial", "lat" : -23.2371177, "lng" : -45.9098362 , "color" : "#CC9966"},
		
		{"type" : "UPA", "type_name" : "Unidades de Pronto Atendimento", "region" : "Leste", "name":"Eugênio de Melo", "address": "Rua Eugênio Augusto de Melo, 101, Eugênio de Melo", "lat" : -23.1375108, "lng" : -45.7837428 , "color" : "#CCCC66" },
		{"type" : "UPA", "type_name" : "Unidades de Pronto Atendimento", "region" : "Leste", "name":"Novo Horizonte", "address": "Rua Tancredo Neves, 5120, Novo Horizonte", "lat" : -23.1901757, "lng" : -45.7877218 , "color" : "#CCCC66"},
		{"type" : "UPA", "type_name" : "Unidades de Pronto Atendimento", "region" : "Norte", "name":"Hospital de Clínicas Norte", "address": "Rua Alziro Lebrão, 76, Alto da Ponte", "lat" : -23.153673, "lng" : -45.901411 , "color" : "#CCCC66"},
		{"type" : "UPA", "type_name" : "Unidades de Pronto Atendimento", "region" : "Norte", "name":"São Francisco Xavier", "address": "Estrada Pedro Davi, s/n, distrito de São Francisco Xavier", "lat" : -22.903279, "lng" : -45.3078729 , "color" : "#CCCC66"},
		{"type" : "UPA", "type_name" : "Unidades de Pronto Atendimento", "region" : "Sul", "name":"Hospital de Clínicas Sul", "address": "Praça Natal, 55, Parque Industrial", "lat" : -23.2371177, "lng" : -45.9098362 , "color" : "#CCCC66"},
		{"type" : "UPA", "type_name" : "Unidades de Pronto Atendimento", "region" : "Sul", "name":"Unidade de Pronto Atendimento de Saúde Mental", "address": "Rua Pituba,100, Jardim Satélite", "lat" : -23.230208, "lng" : -45.88567 , "color" : "#CCCC66"},
		{"type" : "UPA", "type_name" : "Unidades de Pronto Atendimento", "region" : "Sul", "name":"Campo dos Alemães", "address": "Avenida João Oliveira e Silva, s/n, Campos dos Alemães", "lat" : -23.2743877, "lng" : -45.8998474 , "color" : "#CCCC66"},

		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Central" , "name":"Centro I", "address": "Rua Coronel José Monteiro, 407, Centro", "lat" : -23.1824752, "lng" : -45.883907 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Central" , "name":"Centro II", "address": "Avenida Tívoli,195, Vila Betânia", "lat" : -23.2067607, "lng" : -45.8892606 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Central" , "name":"Jardim Paulista", "address": "Rua Martins Pereira, 263, Jardim Paulista", "lat" : -23.1899353, "lng" : -45.8700917 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Central" , "name":"Vila Maria", "address": "Rua São Pedro, 55, Vila Maria", "lat" : -23.1771059, "lng" : -45.8787501 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Central" , "name":"Vila Nair", "address": "Rua Suécia, 50, Vila Nair", "lat" : -23.2109794, "lng" : -45.8852274 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Leste" , "name":"Americano", "address": "Rua Júlia Cursino, 161, Americano", "lat" : -23.1796083, "lng" : -45.8120321 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Leste" , "name":"Campos São José", "address": "Rua Dalila M.Miguez,39, Campos de São José", "lat" : -23.2150557, "lng" : -45.80795879999999 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Leste" , "name":"Eugênio de Melo", "address": "Rua Chico Buquira,411, Galo Branco", "lat" : -23.1333693, "lng" : -45.7701102 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Leste" , "name":"São José II", "address": "Rua Frediano Bianchi Filho, 220, São José II", "lat" : -23.1617969, "lng" : -45.89002079999999 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Leste" , "name":"Nova Detroit", "address": "Avenida José Pedro, 321, Nova Detroit", "lat" : -23.1704289, "lng" : -45.8134366 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Leste" , "name":"Novo Horizonte", "address": "Rua dos Vidraceiros, 159, Novo Horizonte", "lat" : -23.194471, "lng" : -45.7826394 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Leste" , "name":"Paraíso do Sol", "address": "Rua João Gomes Batista Neto, 172, Paraíso do Sol", "lat" : -23.1837559, "lng" : -45.7969895 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Leste" , "name":"Santa Inês II", "address": "Rua dos Cirurgiões Dentistas, 215, Santa Inês II", "lat" : -23.1670176, "lng" : -45.8060054 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Leste" , "name":"Vila Tatetuba", "address": "Rua Mizael Marçal, 190, Vila Industrial", "lat" : -23.1791449, "lng" : -45.8600176 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Leste" , "name":"Vila Tesouro", "address": "Praça Assis Chateubriand, 110, Vila Tesouro", "lat" : -23.2062436, "lng" : -45.900007 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Leste" , "name":"Vista Verde", "address": "Rua Cidade de Brasília, 135, Vista Verde", "lat" : -23.176693, "lng" : -45.8222131 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Norte" , "name":"Altos de Santana", "address": "Avenida Alto do Rio Doce, 1585, Altos de Santana", "lat" : -23.1675195, "lng" : -45.9154815 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Norte" , "name":"Bonsucesso", "address": "Estrada Municipal do Bonsucesso, Km 13, Bonsucesso", "lat" : -23.3125231, "lng" : -45.9093573 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Norte" , "name":"Buquirinha", "address": "Rua José Mendonça da Costa, 82, Buquirinha", "lat" : -23.2581736, "lng" : -45.9106442 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Norte" , "name":"Alto da Ponte", "address": "Rua Anselmo Carnevalli, 82, Alto da Ponte", "lat" : -22.4857949, "lng" : -46.6286789 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Norte" , "name":"Santana", "address": "Avenida Rui Barbosa, 2544, Santana", "lat" : -23.1580512, "lng" : -45.8988681 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Norte" , "name":"São Francisco Xavier", "address": "Estrada Pedro Davi, s/nº, São Francisco Xavier", "lat" : -22.903279, "lng" : -45.3078729 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Norte" , "name":"Telespark", "address": "Rua Benedito Pereira Lima, 210, Telespark", "lat" : -23.1597999, "lng" : -45.909263 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Norte" , "name":"Vila Paiva", "address": "Rua João Pedro da Rocha, 181, Vila Paiva", "lat" : -23.1371823, "lng" : -45.9097485 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Oeste" ,"name":"Jardim das Indústrias", "address": "Rua Pirassununga, 130, Jardim das Indústrias", "lat" : -23.2281366, "lng" : -45.9189617 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Oeste" ,"name":"Limoeiro", "address": "Rua Corifeu A. Marques,3350, Limoeiro", "lat" : -23.2362184, "lng" : -45.9304079 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Sudeste" , "name":"Jardim da Granja", "address": "Rua Urano, 85, Jardim da Granja", "lat" : -23.2065298, "lng" : -45.8569664 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Sudeste" , "name":"Putim", "address": "Rua Roberto Aparecido Cruz, 100, Santo Onofre", "lat" : -23.2484839, "lng" : -45.8325973 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Sudeste" , "name":"São Judas Tadeu", "address": "Rua São Nicolau, 10, São Judas Tadeu", "lat" : -23.2562183, "lng" : -45.8367075 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Sul" , "name":"Bosque dos Eucaliptos", "address": "Rua Maria Palmira Ferreira Ivo, 155, Bosque dos Eucaliptos", "lat" : -23.2503612, "lng" : -45.88700559999999 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Sul" , "name":"Campo Alemães", "address": "Avenida José Izaltino Silva, s/nº, Campos dos Alemães", "lat" : -23.2744125, "lng" : -45.9008613 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Sul" , "name":"Chácaras Reunidas", "address": "Praça Cariri,104, Chácaras Reunidas", "lat" : -23.2553238, "lng" : -45.9239769 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Sul" , "name":"Colonial", "address": "Rua José Ribeiro Bastos, 185, Colonial", "lat" : -23.2787307, "lng" : -45.8976779 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Sul" , "name":"Dom Pedro", "address": "Rua José Eugênio da Silva, 510, Dom Pedro 1º", "lat" : -23.2778337, "lng" : -45.8878285 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Sul" , "name":"Interlagos", "address": "Rua Ubirajara Raimundo de Souza,225, Interlagos", "lat" : -23.2726504, "lng" : -45.8648126 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Sul" , "name":"Morumbi", "address": "Avenida Elisio Galdino Sobrinho, 8, Morumbi", "lat" : -23.2510568, "lng" : -45.9034019 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Sul" , "name":"Oriente", "address": "Rua Senjo Ota, 40, Oriente", "lat" : -23.2446122, "lng" : -45.8953442 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Sul" , "name":"Satélite", "address": "Avenida Andrômeda, 1960, Satélite", "lat" : -23.2299989, "lng" : -45.8845142 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Sul" , "name":"Parque Industrial", "address": "Rua Goiânia, 495, Parque Industrial", "lat" : -23.2375424, "lng" : -45.9086807 , "color" : "#66CC99" },
		{"type" : "UBS" , "type_name" : "Unidades Básicas de Saúde" , "region" : "Sul" , "name":"União", "address": "Rua Marcelo Manso, 55, União", "lat" : -23.2657844, "lng" : -45.90839649999999 , "color" : "#66CC99" }
	]

	for i in lista:
		if posts.find({'type': i['type'], "name" : i['name'] }).count() == 0 :
			db.unifesp.insert(i)

def createDataBaseCIDs():
	with open('cid-10.txt', 'r+') as f:
		grouping = ''
		group_description = ''
		for line in f.readlines():
			line = line.strip()
			s = line.split(') - ')
			s[0] = s[0].replace('(','')
			if '-' in s[0]:
				group = s[0]
				group_description = s[1]
			if '-' not in s[0] and len(s) > 1:
				d = {}
				d['type'] = 'cid'
				d['version'] = 10
				d['code'] = s[0]
				d['neoplasms'] = s[1]
				d['neoplasms_group'] = group
				d['neoplasms_group_description'] = group_description
				# print(d)
				db.unifesp.insert(d)
	f.closed

def createMacroRegions():
	lista = [
		{'type': 'macro_region', 'region': 'Sul', 'university': 3.0, 'bank': 25.0, 'occupied_private_housing': 48927.0, 'lng': -45.8868717948718, 'shopping': 1.0, 'ubs': 8.0, 'delegacy': 2.0, 'hospital': 1.0, 'lat': -23.26710256410257, 'upa': 3.0, 'market': 13.0, 'qtd': 21, 'residents': 163862.0, 'school': 29.0, 'residents_per_household': 70.29999999999998, 'price_by_meter': 3730.5917276622044} ,
		{'type': 'macro_region', 'region': 'Oeste', 'university': 2.0, 'bank': 9.0, 'occupied_private_housing': 11813.0, 'lng': -45.93545945945946, 'shopping': 0.0, 'ubs': 1.0, 'delegacy': 1.0, 'hospital': 0.0, 'lat': -23.20391891891892, 'upa': 0.0, 'market': 4.0, 'qtd': 5, 'residents': 35326.0, 'school': 11.0, 'residents_per_household': 15.100000000000001, 'price_by_meter': 5324.674376240277} ,
		{'type': 'macro_region', 'region': 'Leste', 'university': 0.0, 'bank': 5.0, 'occupied_private_housing': 36229.0, 'lng': -45.80965384615385, 'shopping': 0.0, 'ubs': 13.0, 'delegacy': 1.0, 'hospital': 1.0, 'lat': -23.173038461538454, 'upa': 2.0, 'market': 15.0, 'qtd': 24, 'residents': 125809.0, 'school': 19.0, 'residents_per_household': 82.90000000000002, 'price_by_meter': 3244.0327032589935} ,
		{'type': 'macro_region', 'region': 'Sudeste', 'university': 0.0, 'bank': 1.0, 'occupied_private_housing': 8592.0, 'lng': -45.84732142857144, 'shopping': 0.0, 'ubs': 2.0, 'delegacy': 0.0, 'hospital': 0.0, 'lat': -23.232750000000003, 'upa': 0.0, 'market': 4.0, 'qtd': 9, 'residents': 30464.0, 'school': 4.0, 'residents_per_household': 31.7, 'price_by_meter': 2833.4061504412543} ,
		{'type': 'macro_region', 'region': 'Norte', 'university': 1.0, 'bank': 5.0, 'occupied_private_housing': 14743.0, 'lng': -45.912212121212114, 'shopping': 0.0, 'ubs': 4.0, 'delegacy': 1.0, 'hospital': 1.0, 'lat': -23.146151515151512, 'upa': 1.0, 'market': 5.0, 'qtd': 14, 'residents': 50073.0, 'school': 8.0, 'residents_per_household': 46.900000000000006, 'price_by_meter': 3066.7589758047243} ,
		{'type': 'macro_region', 'region': 'Centro', 'university': 4.0, 'bank': 26.0, 'occupied_private_housing': 16687.0, 'lng': -45.91331578947369, 'shopping': 1.0, 'ubs': 3.0, 'delegacy': 5.0, 'hospital': 1.0, 'lat': -23.196473684210527, 'upa': 0.0, 'market': 8.0, 'qtd': 17, 'residents': 49643.0, 'school': 20.0, 'residents_per_household': 50.5, 'price_by_meter': 4604.609680237176}
	]

	for i in lista:
		if health.find({'type': i['type'], "region" : i['region'] }).count() == 0 :
			db.health.insert(i)

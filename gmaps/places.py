# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import string
import sys
import json
import unicodedata
from decimal import Decimal
import re


from pymongo import MongoClient
import datetime
import json

client = MongoClient('mongodb://localhost:27017/')
db = client.gmaps
collection = db.gmaps
posts = db.health


def stripHTMLTags (html):
	"""
	Strip HTML tags from any string and transfrom special entities
	"""
	import re
	text = html

	# apply rules in given order!
	rules = [
		{ r'>\s+' : u'>'},                  # remove spaces after a tag opens or closes
		{ r'\s+' : u' '},                   # replace consecutive spaces
		{ r'\s*<br\s*/?>\s*' : u'\n'},      # newline after a <br>
		{ r'</(div)\s*>\s*' : u'\n'},       # newline after </p> and </div> and <h1/>...
		{ r'</(p|h\d)\s*>\s*' : u'\n\n'},   # newline after </p> and </div> and <h1/>...
		{ r'<head>.*<\s*(/head|body)[^>]*>' : u'' },     # remove <head> to </head>
		{ r'<a\s+href="([^"]+)"[^>]*>.*</a>' : r'\1' },  # show links instead of texts
		{ r'[ \t]*<[^<]*?/?>' : u'' },            # remove remaining tags
		{ r'^\s+' : u'' }                   # remove spaces at the beginning
	]

	for rule in rules:
		for (k,v) in rule.items():
			regex = re.compile (k)
			text  = regex.sub (v, text)

	# replace special strings
	special = {'&nbsp;' : ' ', '&amp;' : '&', '&quot;' : '"','&lt;'   : '<', '&gt;'  : '>'}

	for (k,v) in special.items():
		text = text.replace (k, v)

	return text


def importPrices(num_pages):
	count = 1
	# result = []
	while count <= num_pages:
		# url = """http://www.redesaojose.com.br/imoveis.php?pg%d&cidade=SAO+JOSE+DOS+CAMPOS&&ipp=30""" % (c)
		url = """http://www.redesaojose.com.br/imoveis.php?pg=%d&finalidade=venda&cidade=SAO+JOSE+DOS+CAMPOS&&ipp=30""" % (count)
		data = urllib.request.urlopen(url)
		soup = BeautifulSoup(data, "lxml")
		items = soup.findAll("div", { "class" : "imovel fullclick tooltip" })
		for i in items:
			d = {}
			info = i.findAll('div',{'class': 'info'})[0]
			if info.text != '':
				local = i.findAll('div',{'class': 'tit'})[0].text.replace('São José Dos Campos ','')
				local = local.split('-')
				if len(local) == 2:
					d["type"] = 'place'
					d["country"] = 'Brasil'
					d["abbreviation_country"] = 'BR'
					d["state"] = 'São Paulo'
					d["abbreviation_state"] = 'SP'
					d["locality"] = 'São José Dos Campos'
					d["neighborhood"] = local[0].strip()
					d["region"] = local[1].strip()
					d["currency"] = 'Real'
					d["abbreviation_currency"] = 'R$'
					try:
						d["price"] = float(i.findAll('div',{'class': 'valor'})[0].text.strip().replace('R$','').strip().replace('.','').replace(',','.'))
						t = info.prettify().replace('\n','').replace('<div class="info">', '').replace('</div>', '').split('<br/>')
						for p in t:
							if 'vaga' in p:
								d["garage"] = int(re.sub(r'^\s+', '', re.sub(r'[^0-9.0-9\[\]]', '', p)))
							elif 'vagas' in p:
								d["garage"] = int(re.sub(r'^\s+', '', re.sub(r'[^0-9.0-9\[\]]', '', p)))
							elif 'dormitórios' in p:
								d["dorms"] = int(re.sub(r'^\s+', '', re.sub(r'[^0-9.0-9\[\]]', '', p)))
							elif 'dormitório' in p:
								d["dorms"] = int(re.sub(r'^\s+', '', re.sub(r'[^0-9.0-9\[\]]', '', p)))
							elif 'privativos' in p:
								d["square_meter"] = int(float(re.sub(r'^\s+', '', re.sub(r'[^0-9.0-9\[\]]', '', p))))
								try:
									db.health.insert(d)
								except Exception as e1:
									pass
					except Exception as e:
						pass
		count += 1
	# return result

# print(importPrices(182))

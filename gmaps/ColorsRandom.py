######################################################
# Funcoes que geram as cores necessários para o sistema
######################################################

# def random_color():
# 	from random import choice
# 	import string
# 	return '%s' % ''.join(choice(string.hexdigits) for x in range(6)).upper()

# def generate_colors(num_colors):
# 	l = []
# 	i = 0
# 	while i < num_colors:
# 		c = random_color()
# 		l.append('#' + str(c))
# 		i += 1
# 	return l

def sinebow(h):
	from math import sin, pi
	h += 1/2
	h *= -1
	r = sin(pi * h)
	g = sin(pi * (h + 1/3))
	b = sin(pi * (h + 2/3))
	return (int(255*chan**2) for chan in (r, g, b))

def nthcolor(n):
	"""
	Gera todas as cores sem repeticao
	function(number) -> list
	"""
	l = []
	phi = (1+5**0.5)/2
	i = 0
	while i < n:
		color = list(sinebow(i * phi))
		if color not in l:
			l.append(color)
			i+=1
	return l

def tohex(colorRGB):
	"""
	Retorna uma cor no formato RGB para Hexadecimal
	function() -> list
	"""
	r = int(colorRGB[0])
	g = int(colorRGB[1])
	b = int(colorRGB[2])
	tu = (r, g, b)
	return '#%02x%02x%02x'.upper() % tu

def generate_colors(num_colors):
	colors = []
	l = list(nthcolor(num_colors))
	for i in l:
		colors.append(tohex(i))
	return colors


colors = []
phi = (1+5**0.5)/2
# Retrieve a single page and report the url and contents
def gen_color(i):
	"""
	Retorna uma cor que não está presente no sistema de busca
	function(number) -> color
	"""
	c = list(sinebow(i * phi))
	c = tohex(c)
	test = True
	global colors
	while test:
		if c not in colors:
			test = False
	return c
	

import random 
def parallel_gen_colors(num_colors):
	"""
	Gera, paralelamente, todas as sem repeticao
	function(number) -> list
	"""
	import concurrent.futures
	l = []
	# We can use a with statement to ensure threads are cleaned up promptly
	with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
		# Start the load operations and mark each future with its URL
		future_to_url = {executor.submit(gen_color, i): i for i in range(num_colors)}
		for future in concurrent.futures.as_completed(future_to_url):
			url = future_to_url[future]
			try:
				data = future.result()
				l.append(data)
				# return data
			except Exception as exc:
				print('%r generated an exception: %s' % (url, exc))
	return l
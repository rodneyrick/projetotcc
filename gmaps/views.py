# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext, Context
from django.core.context_processors import csrf
from django.template.loader import get_template

import datetime
import time
import Geocode
import ColorsRandom
import MongoDB
import k_means
import random
import re
import viewLists
import UploadFiles
import json

# Create your views here.
def index(request):
	regions, table = viewLists.listTableMoreInputs()
	t = get_template('index.html')
	html = t.render(
		Context(
			{
			'regions' : regions,
			'table': table,
			'csrf_token' : csrf(request)['csrf_token']
			}
		)
	)
	html = html.replace("&#39;", "'")
	return HttpResponse(html)

	# return render_to_response(
	# 	'index.html',
	# 	context_instance=RequestContext(request))

def region(request):
	if request.method == 'POST':
		list_points = request.POST.get('new_points').split(';')
		if len(list_points) > 2:
			price = request.POST.get('price')
			color = request.POST.get('color')
			d = {}
			d['type'] = 'region'
			d['price'] = price
			d['color'] = color
			d['LatLng'] = []

			for i in list_points:
				if i != '':
					temp = re.sub(r'^\s+', '', re.sub(r'[^\-0-9.0-9\[\],]', '', i)).split(',')
					d['LatLng'].append([float(temp[0]), float(temp[1])])
			
			MongoDB.insert_item(d)

	colors = [
		['#F7FBFF', '100-500'],
		['#DEEBF7', '500-1000'],
		['#C6DBEF', '1000-1500'],
		['#9ECAE1', '1500-2000'],
		['#6BAED6', '2000-2500'],
		['#4292C6', '2500-3000'],
		['#2171B5', '3000-3500'],
		['#08519C', '3500-4000'],
		['#08306B', '4000-5000'],
		['#08186C', '5000-6000'],
		['#21086C', '6000-10000'],
	]
	regions, table = viewLists.listTableMoreInputs()
	t = get_template('region.html')
	html = t.render(
		Context(
			{'center' : "-23.2062436,-45.900007" ,
			'colors' : colors,
			'regions' : regions,
			'table': table,
			'csrf_token' : csrf(request)['csrf_token']
			}
		)
	)
	html = html.replace("&#39;", "'")
	return HttpResponse(html)

def analysis(request):
	if request.method == 'POST':
		num_centroids = int(request.POST.get('num_centroids'))
		num_points = int(request.POST.get('num_points'))

		pc = MongoDB.list_all_postal_codes()

		list_analysis = []
		i = 0
		while i < num_points:
			r = random.randint(0, (len(pc)-1))
			list_analysis.append(pc.pop(r))
			i += 1

		points, centroids = k_means.k_means_lists(num_centroids, 20, list_analysis)
		dic = k_means.sse(points, centroids)
		regions, table = viewLists.listTableMoreInputs()

		t = get_template('analysis.html')
		html = t.render(
			Context(
				{
				'regions' : regions,
				'table': table,
				'center' : "-23.2062436,-45.900007" ,
				'localizations' : points,
				'colors' : ColorsRandom.generate_colors(num_centroids),
				'centroids' : centroids,
				'sse' : dic,
				'hospitals' : MongoDB.list_all_healths(),
				'csrf_token' : csrf(request)['csrf_token']
				}
			)
		)
		html = html.replace("&#39;", "'")
		return HttpResponse(html)

	# return render_to_response(
	# 	'index.html',
	# 	context_instance=RequestContext(request))
	regions, table = viewLists.listTableMoreInputs()
	t = get_template('index.html')
	html = t.render(
		Context(
			{
			'regions' : regions,
			'table': table,
			'csrf_token' : csrf(request)['csrf_token']
			}
		)
	)
	html = html.replace("&#39;", "'")
	return HttpResponse(html)

def filter(request):
	regions, table = viewLists.listTableMoreInputs()
	t = get_template('filter.html')
	html = t.render(
		Context(
			{
			'regions' : regions,
			'table': table,
			'center' : "-23.2062436,-45.900007",
			'cids_groups' : MongoDB.list_all_cids_groups(),
			'csrf_token' : csrf(request)['csrf_token']
			}
		)
	)
	html = html.replace("&#39;", "'")
	return HttpResponse(html)

def listAllCIDs(request):
	regions, table = viewLists.listTableMoreInputs()
	t = get_template('listAllCIDs.html')
	html = t.render(Context(
			{
			'regions' : regions,
			'table': table,
			'cids' :  viewLists.listAllCIDs(),
			'csrf_token' : csrf(request)['csrf_token']
			}
		)
	)
	html = html.replace("&#39;", "'")
	return HttpResponse(html)

def listAllDocuments(request):
	regions, table = viewLists.listTableMoreInputs()
	t = get_template('listAllDocuments.html')
	html = t.render(Context(
			{'regions' : regions,
			'table': table,
			'documents' :  viewLists.listAllDocuments(),
			'csrf_token' : csrf(request)['csrf_token']}))
	html = html.replace("&#39;", "'")
	return HttpResponse(html)

def listAllHealths(request):
	regions, table = viewLists.listTableMoreInputs()
	hospitals, upas, ubs = viewLists.listAllHealths()
	t = get_template('listAllHealths.html')
	html = t.render(
		Context(
			{'regions' : regions,
			'table': table,
			'hospitals' :  hospitals,
			'upas' : upas,
			'ubs' : ubs,
			'csrf_token' : csrf(request)['csrf_token']}))
	html = html.replace("&#39;", "'")
	return HttpResponse(html)

def listAllPlaces(request):
	regions, table = viewLists.listTableMoreInputs()
	t = get_template('listAllPlaces.html')
	html = t.render(
		Context(
			{'regions' : regions,
			'table': table,
			'places' :  viewLists.listAllPlaces(),
			'csrf_token' : csrf(request)['csrf_token']
			}
		)
	)
	html = html.replace("&#39;", "'")
	return HttpResponse(html)

def uploadFilesToMediaFolder(request):
	regions, table = viewLists.listTableMoreInputs()
	message = ''
	if request.method == 'POST':
		message = UploadFiles.uploadFilesToMediaFolder(request.FILES['upload_file'])
	t = get_template('upload_files.html')
	html = t.render(
		Context(
			{'regions' : regions,
			'table': table,
			'message' : message ,
			'csrf_token' : csrf(request)['csrf_token']}))
	html = html.replace("&#39;", "'")
	return HttpResponse(html)

def locations(request):
	regions, table = viewLists.listTableMoreInputs()

	if request.method == 'POST':
		# center's maps
		num_clusters = int(request.POST.get('num_clusters'))

		colors = ColorsRandom.generate_colors(num_clusters)

		country = request.POST.get('country')
		state = request.POST.get('state')
		city = request.POST.get('city')
		center = Geocode.geocode([country + ' ' + state + ' ' + city, city], isCenter=True)
		center = str(center['lat']) + "," + str(center['lng'])
		
		# ceps's locations
		ceps_list = [ 
			[country + ' ' + 
			state + ' ' +
			city + ' ' +  
			i, i] for i in request.POST.get('ceps').split(';')]

		# items = Geocode.parallelGeocode(ceps_list)
		items = []
		for i in ceps_list:
			items.append(Geocode.geocode(i))

		points, centroids = k_means.k_means_lists(num_clusters, 20, items)

		dic = k_means.sse(points, centroids)

		t = get_template('maps.html')
		html = t.render(
			Context(
				{
				'regions' : regions,
				'table': table,
				'center' : center ,
				'localizations' : points,
				'colors' : colors,
				'centroids' : centroids,
				'sse' : dic,
				'hospitals' : MongoDB.list_all_healths(),
				'csrf_token' : csrf(request)['csrf_token']
				}
			)
		)
		html = html.replace("&#39;", "'")

		return HttpResponse(html)

	# return render_to_response(
	# 	'index.html',
	# 	context_instance=RequestContext(request))

	t = get_template('index.html')
	html = t.render(
		Context(
			{
			'regions' : regions,
			'table': table,
			'csrf_token' : csrf(request)['csrf_token']
			}
		)
	)
	html = html.replace("&#39;", "'")
	return HttpResponse(html)

def maps_regions(request):
	
	regions, table = viewLists.listTableMoreInputs()

	if request.method == 'POST':
		num_points = int(request.POST.get('num_points_regions'))
		moreFields = request.POST.get('moreFields')
		moreFields = json.loads(moreFields)
		cabecalho, result, expression = viewLists.json2matrix(moreFields)
		dic, randomCIDs, dicColors = viewLists.randomCIDs(num_points)
		

		t = get_template('maps_regions.html')
		html = t.render(
			Context({
				'regions' : regions,
				'table': table,
				'macro_regions': viewLists.getDataMacroRegion(),
				'expression' : expression,
				'permission': ['Centro','Leste','Norte','Oeste','Sul','Sudeste'],
				'localizations': randomCIDs,
				'dicData': dic,
				'dicColors': dicColors, 
				'csrf_token' : csrf(request)['csrf_token']
				}
			)
		)
		html = html.replace("&#39;", "'")
		html = html.replace("&lt;", "<")
		html = html.replace("&gt;", ">")
		return HttpResponse(html)

	points = []
	t = get_template('maps_regions.html')
	html = t.render(
		Context({
			'regions' : regions,
			'table': table,
			'macro_regions': viewLists.getDataMacroRegion(),
			'permission': ['Centro','Leste','Norte','Oeste','Sul','Sudeste'],
			'localizations': [],
			'csrf_token' : csrf(request)['csrf_token']
			}
		)
	)
	html = html.replace("&#39;", "'")
	return HttpResponse(html)



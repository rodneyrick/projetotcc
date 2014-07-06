# -*- coding: utf-8 -*-

max_number = 200

def printPoints(coll):
	for i in coll:
		print([i.getCEP(), i.getX(),i.getY(), i.getCluster()])

def printCentroids(coll):
	for i in coll:
		print([i.getNumberOfCluster(), i.getX(),i.getY()])

def distanceEuclidian(pX, pY, cX, cY):
	"""
	Calculate Euclidean distance
	(pX, pY) --> Point's coordanates
	(cX, cY) --> Centroid's coordanates
	"""
	from math import pow, sqrt
	return sqrt(pow((cY - pY), 2) + pow((cX - pX), 2))

def max_min_points_in_maps(points):
	"""
	Return a interval with minimus and maximus positons X, Y
	list --> minX, minY, maxX, minY
	"""
	minX, minY, maxX, maxY = 200.0,200.0,-200.0,-200.0
	for p in points:
		lng = p[1]
		lat = p[0]
		if lng > maxX:
			maxX = lng
		if lat > maxY:
			maxY = lat
		if lng < minX:
			minX = lng
		if lat < minY:
			minY = lat
	return minX, minY, maxX, maxY

def list_points(points):
	"""
	Return a list containing the information points (CEP, Lat, Long, Cluster)
	list --> [Points]
	"""
	return [[p.getCEP(), p.getY(), p.getX(), p.getCluster()] 
		for p in points]

def list_centroids(centroids):
	"""
	Return a list containing the information Centroids (Name Cluster, Lat, Long, Identification Number of the Cluster)
	list --> [Points]
	"""
	return [[ 'Centroid '+  str(c.getNumberOfCluster()), c.getY(), c.getX(), c.getNumberOfCluster()] 
		for c in centroids]

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def setX(self, x):
		self.x = x
	
	def getX(self):
		return self.x
	
	def setY(self, y):
		self.y = x
	
	def getY(self):
		return self.y
	
	def setCluster(self, numberOfCluster):
		self.numberOfCluster = numberOfCluster
	
	def getCluster(self):
		return self.numberOfCluster

class Centroid:
	def __init__(self, x, y, k):
		self.x = x
		self.y = y
		self.k = k
	
	def setX(self, x):
		self.x = x
	
	def getX(self):
		return self.x
	
	def setY(self, y):
		self.y = y
	
	def getY(self):
		return self.y

	def setNumberOfCluster(self, k):
		self.k = k
	
	def getNumberOfCluster(self):
		return self.k

def initialize_centroids(num_clusters, minX, minY, maxX, maxY):
	"""
	Intance list with random Centroids
	list --> [Centroids]
	"""
	from random import uniform
	centroids = []
	# initialize centroids randomly 
	for i in range(num_clusters):
		x = uniform(minX, maxX)
		y = uniform(minY, maxY)
		centroids.append(Centroid(x, y, i))
	return centroids

def reallocate_centroids(points, centroids):
	"""
	Return a repositioning of Centroids
	list --> [Centroids]
	"""
	for c in centroids:
		totalX = 0.0
		totalY = 0.0
		totalInCluster = 0.0
		
		for p in points:
			if(p.getCluster() == c.getNumberOfCluster()):
				totalX += p.getX()
				totalY += p.getY()
				totalInCluster += 1.0
		
		if(totalInCluster > 0):
			c.setX(totalX / totalInCluster)
			c.setY(totalY / totalInCluster)
	return centroids

def initialize_points(ceps_and_coordinates, centroids):
	"""
	Initialization of the coordinates of ceps and allocation in these clusters.
	Returns the list of points.
	list --> [Points]
	"""
	points = []
	for i in ceps_and_coordinates:
		x = i[1]
		y = i[0]
		newPoint = Point(x, y)
		
		bestMinimum = max_number
		currentCluster = 0
		
		# looking for the smallest distance
		for c in centroids:
			distance = distanceEuclidian(x, y, c.getX(), c.getY())
			if(distance < bestMinimum):
				bestMinimum = distance
				currentCluster = c.getNumberOfCluster()
		
		newPoint.setCluster(currentCluster)
		points.append(newPoint)
		reallocate_centroids(points, centroids)
	
	return points

def update_clusters(points, centroids):
	isMoving = 0
	
	for p in points:
		bestMinimum = max_number
		currentCluster = 0
		
		for c in centroids:
			distance = distanceEuclidian(p.getX(), p.getY(), c.getX(), c.getY())
			if(distance < bestMinimum):
				bestMinimum = distance
				currentCluster = c.getNumberOfCluster()
		
		if(p.getCluster() is None or p.getCluster() != currentCluster):
			p.setCluster(currentCluster)
			isMoving = 1
	
	return isMoving, centroids

def k_means(num_clusters, max_iter, points):
	isMoving = 1
	count = 0
	
	# Search the minimum and maximum coordinates for initialization of the centroids perimeter
	minX, minY, maxX, maxY = max_min_points_in_maps(points)

	# creates a list of centroids
	centroids = initialize_centroids(num_clusters, minX, minY, maxX, maxY)
	
	data = initialize_points(points, centroids)
	
	while isMoving and count < max_iter:
		reallocate_centroids(data, centroids)
		isMoving, centroids = update_clusters(data, centroids)
		count += 1

	# printPoints(data)
	# print()
	# printCentroids(centroids)
	return data, centroids

def k_means_lists(num_clusters, max_iter, points):
	"""
	Return Points and Centroids formatted
	list --> Points, Centroids
	"""
	data, centroids = k_means(num_clusters, max_iter, points)
	data = list_points(data)
	centroids = list_centroids(centroids)
	return data, centroids

def sse(points, centroids):
	"""
	Return Error Sum of Squares for each Centroid
	"""
	dic = {}
	i = 0
	for c in centroids:
		dic[i] = 0.0
		for p in points:
			dic[i] += distanceEuclidian(p[2], p[1], c[2], c[1])
		dic[i] = '%.3f' % dic[i]
		i += 1
	return dic

def neighborhood_silhouette(centroids):
	dc = {}
	for i in centroids:
		dc[i[0]] = {'viz': 0, 'dist': 20000.0}

	for i in centroids:
		for j in centroids:
			if i[0] != j[0]:
				dist = distanceEuclidian(i[1], i[2], j[1], j[2])
				if dc[i[0]]['dist'] > dist:
					dc[i[0]]['dist'] = dist
					dc[i[0]]['viz'] = j[0]
	
	return dc
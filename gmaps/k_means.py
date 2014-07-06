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
		lng = p['lng']
		lat = p['lat']
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
	def __init__(self, x, y, cep):
		self.x = x
		self.y = y
		self.cep = cep
	
	def setX(self, x):
		self.x = x
	
	def getX(self):
		return self.x
	
	def setY(self, y):
		self.y = x
	
	def getY(self):
		return self.y

	def getCEP(self):
		return self.cep
	
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
		x = i['lng']
		y = i['lat']
		cep = i['postal_code']
		newPoint = Point(x, y, cep)
		
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


# centroids = [
# 	[0, -45.822369192000004, -23.178613272000003],
# 	[1, -45.87350202689665, -23.186132722758583],
# 	[2, -45.90267284285714, -23.16323995],
# 	[3, -45.86423095625, -23.22301226875]]

# points = [['12201-401', -45.8743338, -23.185098, 1], ['12201-756', -45.8743338, -23.185098, 1], ['12220-183', -45.851709, -23.1851625, 1], ['12201-996', -45.8743338, -23.185098, 1], ['12208-364', -45.8743338, -23.185098, 1], ['12220-915', -45.851709, -23.1851625, 1], ['12201-873', -45.8743338, -23.185098, 1], ['12227-108', -45.851709, -23.2134994, 3], ['12202-166', -45.8743338, -23.185098, 1], ['12220-485', -45.851709, -23.1851625, 1], ['12202-180', -45.8743338, -23.185098, 1], ['12210-961', -45.882583, -23.1841936, 1], ['12203-175', -45.8743338, -23.185098, 1], ['12211-978', -45.8920866, -23.1639035, 2], ['12215-699', -45.868331, -23.1886389, 1], ['12216-197', -45.8778318, -23.1966989, 1], ['12209-938', -45.8635813, -23.2200353, 3], ['12224-584', -45.81610999999999, -23.1702909, 0], ['12213-050', -45.9117949, -23.1583321, 2], ['12201-656', -45.8743338, -23.185098, 1], ['12200-948', -45.8743338, -23.185098, 1], ['12217-429', -45.8743338, -23.185098, 1], ['12221-467', -45.8398398, -23.1739091, 0], ['12216-877', -45.8778318, -23.1966989, 1], ['12207-980', -45.8743338, -23.185098, 1], ['12204-052', -45.8743338, -23.185098, 1], ['12225-145', -45.7805375, -23.1837333, 0], ['12200-119', -45.8743338, -23.185098, 1], ['12211-502', -45.8920866, -23.1639035, 2], ['12219-545', -45.8743338, -23.185098, 1], ['12216-134', -45.8778318, -23.1966989, 1], ['12211-086', -45.8920866, -23.1639035, 2], ['12203-085', -45.8743338, -23.185098, 1], ['12214-040', -45.9139945, -23.167515, 2], ['12201-643', -45.8743338, -23.185098, 1], ['12204-268', -45.8743338, -23.185098, 1], ['12223-725', -45.8232277, -23.184596, 0], ['12210-573', -45.882583, -23.1841936, 1], ['12225-728', -45.7805375, -23.1837333, 0], ['12200-200', -45.8743338, -23.185098, 1], ['Campos', -45.8882128, -23.2396027, 3], ['12225-080', -45.8131951, -23.178453, 0], ['12206-938', -45.8743338, -23.185098, 1], ['12204-075', -45.8743338, -23.185098, 1], ['12203-904', -45.8743338, -23.185098, 1], ['12214-150', -45.9136344, -23.1620422, 2], ['12221-712', -45.8398398, -23.1739091, 0], ['12201-923', -45.8743338, -23.185098, 1], ['12214-680', -45.9182314, -23.1707029, 2], ['12203-855', -45.8743338, -23.185098, 1], ['12203-200', -45.8743338, -23.185098, 1], ['12203-385', -45.8743338, -23.185098, 1], ['12200-730', -45.8743338, -23.185098, 1], ['12207-222', -45.8743338, -23.185098, 1], ['12202-479', -45.8743338, -23.185098, 1], ['12202-350', -45.8743338, -23.185098, 1], ['12209-422', -45.8635813, -23.2200353, 3], ['12201-366', -45.8743338, -23.185098, 1], ['12203-951', -45.8743338, -23.185098, 1], ['12217-099', -45.8743338, -23.185098, 1], ['12216-104', -45.8778318, -23.1966989, 1], ['12207-549', -45.8743338, -23.185098, 1], ['12211-053', -45.8920866, -23.1639035, 2], ['12233-568', -45.882583, -23.2408879, 3], ['12223-211', -45.8232277, -23.184596, 0], ['12216-908', -45.8778318, -23.1966989, 1], ['12218-007', -45.8743338, -23.185098, 1], ['12205-619', -45.8743338, -23.185098, 1], ['12202-898', -45.8743338, -23.185098, 1], ['12224-787', -45.81610999999999, -23.1702909, 0], ['12221-833', -45.8398398, -23.1739091, 0], ['12201-724', -45.8743338, -23.185098, 1], ['12219-189', -45.8743338, -23.185098, 1], ['12202-367', -45.8743338, -23.185098, 1], ['12221-835', -45.8398398, -23.1739091, 0], ['12203-016', -45.8743338, -23.185098, 1], ['12224-416', -45.81610999999999, -23.1702909, 0], ['12245-719', -45.8908986, -23.1930176, 1], ['12203-844', -45.8743338, -23.185098, 1], ['12205-423', -45.8743338, -23.185098, 1], ['12218-638', -45.8743338, -23.185098, 1], ['12226-718', -45.8149585, -23.2137578, 0], ['12218-014', -45.8743338, -23.185098, 1], ['12208-025', -45.8743338, -23.185098, 1], ['12221-614', -45.8398398, -23.1739091, 0], ['12223-006', -45.8232277, -23.184596, 0], ['12200-145', -45.8743338, -23.185098, 1], ['12211-974', -45.8920866, -23.1639035, 2], ['12215-927', -45.868331, -23.1886389, 1], ['12216-399', -45.8778318, -23.1966989, 1], ['12201-361', -45.8743338, -23.185098, 1], ['12203-726', -45.8743338, -23.185098, 1], ['12201-178', -45.8743338, -23.185098, 1], ['12204-807', -45.8743338, -23.185098, 1], ['12227-325', -45.851709, -23.2134994, 3], ['12201-473', -45.8743338, -23.185098, 1], ['12214-869', -45.9182314, -23.1707029, 2], ['12215-813', -45.868331, -23.1886389, 1], ['12217-486', -45.8743338, -23.185098, 1], ['12219-352', -45.8743338, -23.185098, 1], ['12215-511', -45.868331, -23.1886389, 1], ['12202-439', -45.8743338, -23.185098, 1], ['12223-300', -45.834217, -23.1823047, 0], ['12215-767', -45.868331, -23.1886389, 1], ['12225-173', -45.7805375, -23.1837333, 0], ['12206-400', -45.8743338, -23.185098, 1], ['12206-645', -45.8743338, -23.185098, 1], ['12227-495', -45.851709, -23.2134994, 3], ['12223-139', -45.8232277, -23.184596, 0], ['12221-628', -45.8398398, -23.1739091, 0], ['12201-170', -45.8743338, -23.185098, 1], ['12216-410', -45.86911990000001, -23.1922444, 1], ['12205-943', -45.8743338, -23.185098, 1], ['12205-690', -45.8743338, -23.185098, 1], ['12201-647', -45.8743338, -23.185098, 1], ['12209-802', -45.8635813, -23.2200353, 3], ['12218-393', -45.8743338, -23.185098, 1], ['12203-100', -45.8743338, -23.185098, 1], ['12203-551', -45.8743338, -23.185098, 1], ['12213-580', -45.902715, -23.1405578, 2], ['12202-251', -45.8743338, -23.185098, 1], ['12200-142', -45.8743338, -23.185098, 1], ['12202-740', -45.8743338, -23.185098, 1], ['12207-930', -45.8743338, -23.185098, 1], ['12220-859', -45.851709, -23.1851625, 1], ['12216-734', -45.8778318, -23.1966989, 1], ['12208-582', -45.8743338, -23.185098, 1], ['12209-055', -45.8635813, -23.2200353, 3], ['12209-609', -45.8635813, -23.2200353, 3], ['12201-041', -45.8743338, -23.185098, 1], ['12206-297', -45.8743338, -23.185098, 1], ['12211-269', -45.8920866, -23.1639035, 2], ['12209-196', -45.8635813, -23.2200353, 3], ['12209-511', -45.8635813, -23.2200353, 3], ['12217-378', -45.8743338, -23.185098, 1], ['12217-289', -45.8743338, -23.185098, 1], ['12203-870', -45.8743338, -23.185098, 1], ['12207-975', -45.8743338, -23.185098, 1], ['12201-396', -45.8743338, -23.185098, 1], ['12220-850', -45.851709, -23.1851625, 1], ['12217-064', -45.8743338, -23.185098, 1], ['12218-130', -45.8743338, -23.185098, 1], ['12222-401', -45.8743338, -23.185098, 1], ['12219-219', -45.8743338, -23.185098, 1], ['12202-823', -45.8743338, -23.185098, 1], ['12221-868', -45.8398398, -23.1739091, 0], ['12207-868', -45.8743338, -23.185098, 1], ['12216-510', -45.8805366, -23.196675, 1], ['12205-059', -45.8743338, -23.185098, 1], ['12200-240', -45.8743338, -23.185098, 1], ['12209-447', -45.8635813, -23.2200353, 3], ['12209-074', -45.8635813, -23.2200353, 3], ['12200-021', -45.8743338, -23.185098, 1], ['12201-477', -45.8743338, -23.185098, 1], ['12203-487', -45.8743338, -23.185098, 1], ['12203-280', -45.8743338, -23.185098, 1], ['12219-212', -45.8743338, -23.185098, 1], ['12201-615', -45.8743338, -23.185098, 1], ['12220-689', -45.851709, -23.1851625, 1], ['12221-186', -45.8398398, -23.1739091, 0], ['12220-161', -45.851709, -23.1851625, 1], ['12206-397', -45.8743338, -23.185098, 1], ['12201-839', -45.8743338, -23.185098, 1], ['12201-776', -45.8743338, -23.185098, 1], ['12221-611', -45.8398398, -23.1739091, 0], ['12200-492', -45.8743338, -23.185098, 1], ['12214-010', -45.914212, -23.1681819, 2], ['12200-162', -45.8743338, -23.185098, 1], ['12203-056', -45.8743338, -23.185098, 1], ['12207-719', -45.8743338, -23.185098, 1], ['12202-068', -45.8743338, -23.185098, 1], ['12202-133', -45.8743338, -23.185098, 1], ['12201-253', -45.8743338, -23.185098, 1], ['12232-254', -45.8778318, -23.2533904, 3], ['12202-795', -45.8743338, -23.185098, 1], ['12203-975', -45.8743338, -23.185098, 1], ['12202-306', -45.8743338, -23.185098, 1], ['12219-658', -45.8743338, -23.185098, 1], ['12222-730', -45.8743338, -23.185098, 1], ['12218-582', -45.8743338, -23.185098, 1], ['12216-234', -45.8778318, -23.1966989, 1], ['12217-379', -45.8743338, -23.185098, 1], ['12216-953', -45.8778318, -23.1966989, 1], ['12200-160', -45.8743338, -23.185098, 1], ['12217-286', -45.8743338, -23.185098, 1], ['12224-411', -45.81610999999999, -23.1702909, 0], ['12202-503', -45.8743338, -23.185098, 1], ['12227-096', -45.851709, -23.2134994, 3], ['12215-361', -45.868331, -23.1886389, 1], ['12201-405', -45.8743338, -23.185098, 1], ['12206-481', -45.8743338, -23.185098, 1], ['12219-747', -45.8743338, -23.185098, 1], ['12202-135', -45.8743338, -23.185098, 1], ['12223-343', -45.8232277, -23.184596, 0], ['12204-894', -45.8743338, -23.185098, 1], ['12202-820', -45.8743338, -23.185098, 1], ['12222-547', -45.8743338, -23.185098, 1], ['12211-374', -45.8920866, -23.1639035, 2], ['12210-371', -45.882583, -23.1841936, 1], ['12224-408', -45.81610999999999, -23.1702909, 0]]


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

# neighborhood = neighborhood_silhouette(centroids)

# dp = {}
# for i in points:
# 	for j in points:
		

# 	if 'n' in neighborhood[i[3]]:
# 		neighborhood[i[3]]['n'] += 1
# 		neighborhood[i[3]]['lat'] += i[2]
# 		neighborhood[i[3]]['lng'] += i[1]
# 		neighborhood[i[3]]['silhueta'] += distanceEuclidian(
# 			i[1], i[2],
# 			centroids[i[3]][1], centroids[i[3]][2]
# 		)
# 	else:
#         neighborhood[i[3]] = {
# 			'n':1, 
# 			'lat' : i[2], 
# 			'lng' : i[1],
# 			'silhueta_a' : distanceEuclidian(
# 				i[1], i[2],
# 				centroids[i[3]][1], centroids[i[3]][2]
# 			)
# 		}


# import json
# print(json.dumps(neighborhood, sort_keys=True, indent=4))
# print(json.dumps(dp, sort_keys=True, indent=4))

# # for c in neighborhood:
# # 	for p in points:
# # 		if p[1] == neighborhood[c]:
# # 			dp[c]['silhueta_b'] += distanceEuclidian(
# # 				p[1], p[2],
# # 				centroids[i[3]][1], centroids[i[3]][2]
# # 			)



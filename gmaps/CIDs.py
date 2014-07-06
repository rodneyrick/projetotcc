
import MongoDB

def CID(list_code):
	f = open('workfile.txt', 'w')
	for c in list_code:
		time.sleep(5)
		url = """http://www.bulas.med.br/cid-10/index.asp?act=Search&_id_=186&Code=""" + c
		# print(url)
		data = urllib.request.urlopen(url)
		soup = BeautifulSoup(data, "lxml")
		items = soup.findAll("tr", { "class" : ["odd", "even"] })
		for i in items:
			cells = i.findAll("a")
			f.write(cells[0].text)
			f.write(' - ')
			f.write(cells[1].text)
			f.write('\n')
		f.flush()
	f.closed

# cids = ["C%02d" % a for a in range(98)] + ["D%02d" % a for a in range(49)]
# CID(cids)

def createDataBaseCIDs():
	with open('cid-10.txt', 'r+') as f:
		grouping = ''
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
				MongoDB.insert_item(d)
	f.closed

def randomCIDs(num_max_cids):
	import random
	listCIDs = MongoDB.list_all_cids()
	list_analysis = []
	i = 0
	while i < num_max_cids:
		r = random.randint(0, (len(listCIDs)-1))
		list_analysis.append(listCIDs[r]['code'])
		i += 1
	# print(len(list_analysis))
	# print(len(set(list_analysis)))
	return list_analysis

createDataBaseCIDs()
# -*- coding: utf-8 -*-

import datetime
import time
import MongoDB
import random
import re

def uploadFilesToMediaFolder(fileItem):
	t = int(time.time())
	filename = '%s_%s' % (str(t), fileItem)
	d = {}
	d["type"] = "file"
	d["extension"] = str(filename.split('.')[-1])
	d["name"] = str(filename)
	d["date"] = t
	MongoDB.insert_item(d)
	path = 'media/%s' % (filename)
	destination = open(path, 'wb+')
	message = 'Upload feito com sucesso!'
	for chunk in fileItem.chunks():
		destination.write(chunk)
	destination.close()
	return message
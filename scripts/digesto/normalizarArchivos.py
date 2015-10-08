#!/usr/bin/python

import os, sys, re
import shutil

def getFileNormalize(fileName):
	patron = re.compile('([a-zA-Z]+).*?([0-9]+).*?-.*?([0-9]{1,4}).*')
	m = patron.match(fileName)
	if m is None:
		return None
	list = m.groups()
	return '{}-{}-{}.pdf'.format(list[0].lower(),list[1],list[2])

def getFiles(basepath):
	files = []
	for fname in os.listdir(basepath):
		path = os.path.join(basepath, fname)
		if os.path.isdir(path):
			files.extend(getFiles(path))
			continue
		fnorm = getFileNormalize(fname)
		if fnorm is not None:
			files.append([path,fnorm])
	return files


basepath = '/home/emanuel/ownCloud/digesto-resoluciones/DIGESTO'
destpath = '/home/emanuel/resoluciones/'

files = getFiles(basepath)
for file in files:
	dest = destpath + file[1]
	print ('Origen {} destino {}'.format(file[0],dest))
	shutil.copy2(file[0], dest)

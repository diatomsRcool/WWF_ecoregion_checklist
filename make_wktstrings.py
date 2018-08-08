"""
#I used this bit of code to see how many unique ecoregions were in the data set = 827
import pickle

in_file = open('ecoregion_polygons.tsv', 'r')

ecoregions = []

for line in in_file:
	row = line.split('\t')
	ecoregion = row[1]
	if ecoregion in ecoregions:
		continue
	else:
		ecoregions.append(ecoregion)
print(len(ecoregions))
pickle.dump(ecoregions, open('ecoregion_list.p', 'wb'))
"""
#This code takes the wkt strings make from each polygon in parse_polygon.py and makes
#one wkt string for each ecoregion.

import pickle
import re

in_file = open('ecoregion_polygons.tsv', 'r')
f = open('ecoregion_list.p', 'rb')
out_file = open('all_wkt_string.tsv', 'w')

ecoregions = pickle.load(f)

for e in ecoregions:
	print(e)
	string = 'GEOMETRYCOLLECTION%28'
	in_file.seek(0)
	for line in in_file:
		line = line.strip('\n')
		row = line.split('\t')
		id = row[0]
		ecor = row[1]
		polygon = row[2]
		#print(id)
		if ecor == e:
			string = string + polygon + '%2C'
			counter = counter + 1
		else:
			continue
	string = string.strip('%2C')
	string = string + '%29'
	e = re.sub(' ', '_', e)
	out_file.write(e + '\t' + string + '\n')


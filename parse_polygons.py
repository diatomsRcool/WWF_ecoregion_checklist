#this code iterates over the WWF ecoregion file downloaded from google and translates
#each polygon into a wkt string, then outputs to a separate file. Each row in the csv
#file is a single polygon. Each ecoregion can have multiple rows. The output file is a 
#wkt string for each row/polygon.


import csv
import sys
import re

csv.field_size_limit(sys.maxsize)

#long/lat

in_file = open('WWF Ecoregions.csv', 'r')
out_file = open('ecoregion_polygons.tsv', 'w')

kml = csv.reader(in_file, quotechar = '"')
next(kml)
for row in kml:
	polygon = row[0].split(' ')
	ecoregion = row[5]
	id = row[2]
	print(id)
	string = 'POLYGON(('
	for v in polygon:
		v = re.sub('<Polygon><outerBoundaryIs><LinearRing><coordinates>', '', v)
		v = re.sub('</coordinates></LinearRing></outerBoundaryIs></Polygon>', '', v)
		m = v.split(',')
		long = round(float(m[0]), 3)
		lat = round(float(m[1]), 3)
		string = string + str(long) + '%20' + str(lat) + '%2C%20'
	string = re.sub('%2C%20$', '))', string)
	#string = string + '))'
	out_file.write(id + '\t' + ecoregion + '\t' + string + '\n')
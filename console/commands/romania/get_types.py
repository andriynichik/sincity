# encoding=utf8
import csv
from lib.config.Yaml import Yaml as Config
import pandas as pd
import time
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.spider.Spider import Spider
from lib.parser.map.google.GMapFactory import GMapFactory as MapFactory
from lib.factory.Loader import Loader as LoaderFactory
from lib.parser.wiki.Spain import Spain as WikiES
from lib.factory.Loader import Loader 
import math
import sys
import hashlib
from lib.logger.File import File as FileLog
from argparse import ArgumentParser
import sys
import json
import requests
import pymongo
from bson.json_util import dumps
from lib.keygen.gmap_keygen import Keygen



# from lib.parser.wiki.Spain import Spain as ParserSpain
country = 'Spain'
config = Config('./config/config.yml')
mongo_config = config.get('mongodb')
conn = pymongo.MongoClient(mongo_config['host'], mongo_config['port'])
Key = Keygen()
cnf = {'geocoding':{'key': Key.get_key_geocode()}}
config.set(cnf)
db = conn.location
coll = db.sinoplik_romania
# print(config.get('googlemaps').get('geocoding').get('key'))
doc_factory = DocFactory(config.get('mongodb'))
# try:
# 	skiprows = sys.argv[1]
# except Exception as e:
# 	skiprows = 0
# df = pd.read_csv('./data/spain/Spain_notDublicate.csv',  skiprows=int(skiprows), low_memory=False)
loader = Loader.loader_with_mongodb(config.get('mongodb'))
headers = {'User-Agent': 'Mozilla/5.0'}


language='ro'
# spider = Spider(
#     loader_factory=LoaderFactory,
#     gmap_parser=MapFactory.spain,
#     wiki_parser=True,
#     doc_factory=doc_factory,
#     language=language,
#     config=config,
#     use_cache=True
# )



def getDistance(lat1,lon1,lat2,lon2):
    Key = Keygen()
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&mode=walking&origins='+str(lat1)+','+str(lon1)+'&destinations='+str(lat2)+','+str(lon2)+'&key='+str(Key.get_key_distance())+''
    print(url)
    response = requests.get(url)
    data = response.json()
    try:
        resp = data['rows'][0]['elements'][0]['distance']['value'] / 1000
    except Exception as e:
        resp = 0
    
    print (round(resp, 2))
    return round(resp, 2)


	
datar = db.sinoplik_romania.find()
for row in datar:
	
	
	try:
		

		if  'parser_id' in row:
			obj = db.romania.find_one({"_id": row['parser_id']})
			
			db.sinoplik_romania.update_one(
						                {"_id": row['_id'] },
						                    {
						                        "$set": {
						                        'parser_type':obj['TIP']
						                        
						                    }
						               }
						        )
			print (obj['TIP'])
	# try:
	# 	print(row)
	# 	if  row and "wiki_center" in row and "gmap_center" in row:
	# 		# data =  getDistance(row["gmap_center"]["lat"],row["gmap_center"]["lng"], row["wiki_center"]["lat"],row["wiki_center"]["lng"])
	# 		if not 'gmap_wiki_distance' in row:
				
	# 		# print(row["gmap_center"]["lat"],row["gmap_center"]["lng"], row["wiki_center"]["lat"],row["wiki_center"]["lng"])
	# 			distance =  getDistance(row["gmap_center"]["lat"],row["gmap_center"]["lng"], row["wiki_center"]["lat"],row["wiki_center"]["lng"])
	# 			print(distance)
				# db.sinoplik_romania.update_one(
				# 	                {"_id": row['_id'] },
				# 	                    {
				# 	                        "$set": {
					                       	
				# 	                       	'gmap_wiki_distance': distance,
					                        
				# 	                    }
				# 	               }
				# 	        )
			

	except Exception as e:
		print(str(e))



	# geocode

	# AIzaSyDNdfjGqet-urajuNutvAphLKkdGNPb0tU
	
	# distance
	# AIzaSyDwMgSt7YSWui3RyW9jGbklwakm6ck1AFc
	# AIzaSyAHJ34GoC1EsMfGT5H2N-BmOUbz1XIGKCc

	# placec
	# AIzaSyDhGBybrx1Ir94MmmMpYYgpJASvZS3TVLE
	# AIzaSyAI16xrjPDt9IRmtu8dl5VgxOhZG-hVRrc



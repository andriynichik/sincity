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
from bson.objectid import ObjectId


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
	if 'parser_id' in row:
		thistype = db.romania.find_one({"_id" : ObjectId(row['parser_id'])})
		if 'gmap_type' in thistype:
			if thistype['gmap_type'] == 'locality':
				pass
		
	# thistype
	# obj = db.romania.find_one({"DENLOC":row['title'].upper()})
				print (thistype['gmap_type'], row['title'].upper())
			else:
				region = {
					"2502":"8",
					"2460":"8",
					"2495":"7",
					"2466":"7",
					"2497":"7",
					"2475":"7",
					"2474":"7",
					"2501":"7",
					"2471":"1",
					"2478":"1",
					"2491":"1",
					"2483":"1",
					"2481":"1",
					"2467":"1",
					"2488":"6",
					"2470":"6",
					"2461":"6",
					"2476":"6",
					"2479":"6",
					"2496":"6",
					"2473":"3",
					"2494":"3",
					"2487":"3",
					"2492":"3",
					"2468":"3",
					"2500":"3",
					"2499":"3",
					"2469":"2",
					"2477":"2",
					"2482":"2",
					"2465":"2",
					"2498":"2",
					"2464":"2",
					"2486":"2",
					"2480":"4",
					"2485":"4",
					"2463":"4",
					"2484":"4",
					"2490":"4",
					"2472":"5",
					"2489":"5",
					"2462":"5",
					"2493":"5",
				}
				my_reg = region[str(row['region_id'])]	
				print(my_reg)
				obj = db.romania.find_one({"DENLOC":row['title'].upper(), "gmap_type":"locality", "REGIUNE": int(my_reg)})
		
				if obj is not None and 'wiki_center' in obj:
					distance =  getDistance(row["lat"],row["lng"], obj["wiki_center"]["lat"],obj["wiki_center"]["lng"])
					comparison_url =("https://www.google.com.ua/maps/dir/"+str(row['lat'])+","+str(row['lng'])+"/"+str(obj["wiki_center"]["lat"])+","+str(obj["wiki_center"]["lng"])+"")

					db.sinoplik_romania.update_one(
								                {"_id": row['_id'] },
								                    {
								                        "$set": {
								                       	'parser_id': obj['_id'],
								                       	'DENLOC':obj['DENLOC'],
								                       	'comparison': distance,
								                       	'comparison_url':comparison_url
								                        
								                    }
								               }
								        )
				elif obj is not None and '_id' in obj:
					db.sinoplik_romania.update_one(
								                {"_id": row['_id'] },
								                    {
								                        "$set": {
								                       	'parser_id': obj['_id'],
								                       	'DENLOC':obj['DENLOC'],
								                       	
								                        
								                    }
								               }
								        )
				else:
					db.sinoplik_romania.update_one(
								                {"_id": row['_id'] },
								                    {
								                        "$unset": {
								                       	'parser_id': row['_id'],
								                       	'DENLOC':row['DENLOC'],
								                     	'comparison': distance,
								                       	'comparison_url':comparison_url
								                       	
								                        
								                    }
								               }
								        )

	# try:
	# 	pass

	# 	# if  'wiki_center' in obj:
	# 	# 	distance =  getDistance(row["lat"],row["lng"], obj["wiki_center"]["lat"],obj["wiki_center"]["lng"])
	# 	# 	comparison_url =("https://www.google.com.ua/maps/dir/"+str(row['lat'])+","+str(row['lng'])+"/"+str(obj["wiki_center"]["lat"])+","+str(obj["wiki_center"]["lng"])+"")

	# 	# 	db.sinoplik_romania.update_one(
	# 	# 				                {"_id": row['_id'] },
	# 	# 				                    {
	# 	# 				                        "$set": {
	# 	# 				                       	'parser_id': obj['_id'],
	# 	# 				                       	'DENLOC':obj['DENLOC'],
	# 	# 				                       	'comparison': distance,
	# 	# 				                       	'comparison_url':comparison_url
						                        
	# 	# 				                    }
	# 	# 				               }
	# 	# 				        )
	# 	# elif '_id' in obj:
	# 	# 	db.sinoplik_romania.update_one(
	# 	# 				                {"_id": row['_id'] },
	# 	# 				                    {
	# 	# 				                        "$set": {
	# 	# 				                       	'parser_id': obj['_id'],
	# 	# 				                       	'DENLOC':obj['DENLOC'],
						                       	
						                        
	# 	# 				                    }
	# 	# 				               }
	# 	# 				        )
	# except Exception as e:
	# 	print(str(e))




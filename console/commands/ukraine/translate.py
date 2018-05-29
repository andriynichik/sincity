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
db = conn.location
coll = db.SPAININE
print(config.get('googlemaps').get('geocoding').get('key'))
doc_factory = DocFactory(config.get('mongodb'))
try:
	skiprows = sys.argv[1]
except Exception as e:
	skiprows = 0
df = pd.read_csv('./data/spain/Spain_notDublicate.csv',  skiprows=int(skiprows), low_memory=False)
loader = Loader.loader_with_mongodb(config.get('mongodb'))
headers = {'User-Agent': 'Mozilla/5.0'}


# language='es'

def getTranslate(place_id):


	Key = Keygen()
	translate = {}
	languages = ["uk","ru","ca", "lv","en","pl" ,"de",  "fr" , "it", "es", "ro", "nl", "el" , "cs", "pt", "hu" , "sv", "bg", "sr", "da", "fi", "sk", "sl", "hr", "lt"]
	for lang in languages:
		keyAPI = Key.get_key_geocode()
		if not keyAPI:
			sys.exit()	
	

		cnf = {'googlemaps':{'geocoding':{'key': keyAPI}}}
		config.set(cnf)

		spider = Spider(
		    loader_factory=LoaderFactory,
		    gmap_parser=MapFactory.spain,
		    wiki_parser=True,
		    doc_factory=doc_factory,
		    
		    config=config,
		    use_cache=True
		)
		spider.gmap_loader._language = lang
		objects = spider.get_gmap_place_id(place_id)
		gmap = {}
		if objects:
			gmap = objects[0].get_document()
			translate[lang] = {'name': gmap.get('name'), 
						 	   
						 	   }
	return translate




config = Config('./config/config.yml')
mongo_config = config.get('mongodb')
connection = pymongo.MongoClient(mongo_config['host'], mongo_config['port'])
db = connection.location
try:
	
	for doc in db.ukraine_city_sublocal.find({}, no_cursor_timeout=True):
		try:

			place_id = doc['code']
			translate_data = getTranslate(place_id)
			print (translate_data)
			db.ukraine_city_sublocal.update_one(
				                {"_id": doc['_id']},
				                    {
				                        "$set": {
				                        "translate": translate_data
				
				                        
				                    }
				               }
				        )
			# print (doc['12_gmap_type'])
			# types = {"Municipio": "administrative_area_level_4",
			# 		"Entidad colectiva" :  "administrative_area_level_5",
			# 		"Otras entidades": "locality",
			# 		"Capital de municipio": "locality",
			# 		"Entidad singular": "locality" }
			# if doc['12_gmap_type'] == types[doc['25_SNIG_TIPO']]:
			# 	print("YESSS")
			# else:
			# 	print("Noooooooo")
			# 	# types = {"Municipio": "administrative_area_level_4",
			# 	# 	"Entidad colectiva" :  "administrative_area_level_5",
			# 	# 	"Otras entidades": "locality",
			# 	# 	"Capital de municipio": "locality",
			# 	# 	"Entidad singular": "locality" } 
			# 	# place = get_place_ids_by_address_for_type
			# 	Key = Keygen()
			# 	keyAPI =  Key.get_key_place()
			# 	if not keyAPI:
			# 		sys.exit()
			# 	cnf = {'googlemaps':{'geocoding':{'key': keyAPI}}}
			# 	config.set(cnf)
			# 	print (keyAPI)
			# 	spider.gmap_loader._language = language
			# 	print (doc['08_INE_Name_w_Article'], types[doc['25_SNIG_TIPO']])
			# 	dta = spider.get_place_ids_by_address_for_type(doc['08_INE_Name_w_Article'] + ', España', types[doc['25_SNIG_TIPO']])
			# 	# gmap = {}
			# 	# if objects:
			# 	# 	gmap = objects[0].get_document()
			# 	if len(dta) > 0:
			# 		place_id = dta[0]
			# 		objects = spider.get_gmap_place_id(place_id)
			# 		gmap = {}
			# 		gmap = objects[0].get_document()
			# 		print (gmap)
			# 		try:
			# 			if gmap['name'].lower().lstrip().strip() == doc['08_INE_Name_w_Article'].lower().lstrip().strip():
			# 				gmap['comparison'] = True
			# 			else:
			# 				gmap['comparison'] = False
			# 		except Exception as e:
			# 			gmap['comparison'] = False

			# 		gmap['15_GMap_center_SNIG_comparison'] = getDistance(gmap['center']['lat'], gmap['center']['lng'],doc['28_SNIG_LATITUD_ETRS89'],doc['29_SNIG_LONGITUD_ETRS89'])
			# 		gmap['15_gmap_comparison_url'] =("https://www.google.com.ua/maps/dir/"+str(gmap['center']['lat'])+","+str(gmap['center']['lng'])+"/"+str(doc['28_SNIG_LATITUD_ETRS89'])+","+str(doc['29_SNIG_LONGITUD_ETRS89'])+"")
			# 		db.internal.update_one(
			#                 {"_id": doc['_id']},
			#                     {
			#                         "$set": {
			#                         "10_gmap_name": gmap.get('name'),
			#                         "17_gmap_admin_hierarchy": gmap.get('admin_hierarchy', {}),
			#                         "gmap_center": gmap.get('center'),
			#                         "gmap_bounds": gmap.get('bounds'),
			#                         "12_gmap_type": gmap.get('type'),
			#                         "15_GMap_center_SNIG_comparison": gmap.get('15_GMap_center_SNIG_comparison'),
			#                         "15_gmap_comparison_url": gmap.get('15_gmap_comparison_url'),
			#                         "11_gmap_comparison" : gmap['comparison']
			                        
			#                     }
			#                }
			#         )
			#         # gmap.pop('_id')
			#         # # gmap['15_GMap_center_SNIG_comparison'] = getDistance(gmap['center']['lat'], gmap['center']['lng'],doc['28_SNIG_LATITUD_ETRS89'],doc['29_SNIG_LONGITUD_ETRS89'])
			#         # if gmap['15_GMap_center_SNIG_comparison'] <= 1:
			#         #     gm_comp_status = True
			#         # else:
			#         #     gm_comp_status = False

			#         # types = {"Municipio": ["administrative_area_level_4"],
			#         #     "Entidad colectiva" :  ["administrative_area_level_5", "neighborhood"],
			#         #     "Otras entidades": ["locality", "neighborhood"],
			#         #     "Capital de municipio":["locality"],
			#         #     "Entidad singular": ["locality"]}
			#         # if gmap.get('type') in types[doc['25_SNIG_TIPO']]:
			#         #     gm_type_status = True
			#         # else:
			#         #     gm_type_status = False

			#         # raw = {
			#         #         "gmap_name": gmap.get('name'),
			#         #         "gmap_name_status" : gmap['comparison'],
			#         #         "gmap_type": gmap.get('type'),
			#         #         "15_GMap_center_SNIG_comparison": gmap.get('15_GMap_center_SNIG_comparison'),
			#         #         "15_gmap_comparison_url": gmap.get('15_gmap_comparison_url'),
			#         #         "gmap_comp_status":gm_comp_status,
			#         #         "gmap_type_status":gm_type_status,

			#         #     }
			# 	print (objects)
		except Exception as e:
			print(str(e))

except Exception as e:
	raise print(str(e))


	print ("===================================================")
	

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
coll = db.SPAININE
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

try:
	

	for row in db.romania.find():
		if "wiki_center" in row and "gmap_center" in row:
			# data =  getDistance(row["gmap_center"]["lat"],row["gmap_center"]["lng"], row["wiki_center"]["lat"],row["wiki_center"]["lng"])
			try:
				print(row["gmap_center"]["lat"],row["gmap_center"]["lng"], row["wiki_center"]["lat"],row["wiki_center"]["lng"])
				distance =  getDistance(row["gmap_center"]["lat"],row["gmap_center"]["lng"], row["wiki_center"]["lat"],row["wiki_center"]["lng"])
				print(distance)
				db.romania.update_one(
			                {"_id": row['_id'] },
			                    {
			                        "$set": {
			                       	
			                       	'gmap_wiki_distance': distance,
			                        
			                    }
			               }
			        )
			except Exception as e:
				print(str(e))

except Exception as e:
	raise e	
		# Key = Keygen()
		# keyAPI =  Key.get_key_geocode()
		# if not keyAPI:
		# 	sys.exit()

		# cnf = {'googlemaps':{'geocoding':{'key': keyAPI}}}
		# config.set(cnf)
		# spider = Spider(
		#     loader_factory=LoaderFactory,
		#     gmap_parser=MapFactory.spain,
		#     wiki_parser=True,
		#     doc_factory=doc_factory,
		#     language=language,
		#     config=config,
		#     use_cache=True
		# )
		# # spider.gmap_loader._language = language

		# print('========================================')
		# adress =  str(row['DENLOC']+' '+str(row['CODP'])+', România')
		# data = gmap_by_address(adress, spider)
		# if 'name' in data:
		# 	print('yessss')
		# 	print(data)
		# else:

		# 	adress =  str(row['DENLOC']+', România')
		# 	data = gmap_by_address(adress, spider)
		# 	print('Nooooooo')
		# 	print(data)
		# print('========================================')
		
		# internal = {}

		# if 'name' in data.keys():
		# 	internal['gmap_name'] = data.get('name')
		# if 'admin_hierarchy' in data.keys():
		# 	internal['gmap_admin_hierarchy']=data.get('admin_hierarchy', {})
		# if 'center' in data.keys():
		# 	internal['gmap_center'] =data.get('center')
		# if 'bounds' in data.keys():
		# 	internal['gmap_bounds'] =data.get('bounds')
		# if 'type' in data.keys():
		# 	internal['type']=data.get('type')
		# if 'translate' in data.keys():
		# 	internal['translate']=data.get('translate')
		# if 'requests' in data.keys():
		# 	internal['requests']=data.get('requests')
		# if 'code' in data.keys():
		# 	internal['code']=data.get('code')
		# if 'postal_code' in data.keys():
		# 	internal['postal_code']=data.get('postal_code')
		# if 'name' in data:
		# 	db.romania.update_one(
		#                 {"_id": row['_id'] },
		#                     {
		#                         "$set": {
		                       	
		#                        	'gmap_name': data.get('name'),
		#                        	'gmap_admin_hierarchy': data.get('admin_hierarchy', {}),
		#                        	'gmap_center': data.get('center'),
		#                        	'gmap_bounds': data.get('bounds'),
		#                        	'gmap_type': data.get('type'),
		#                        	'gmap_translate': data.get('translate'),
		#                        	'gmap_requests': data.get('requests'),
		#                        	'gmap_code': data.get('code'),
		#                        	'gmap_postal_code': data.get('postal_code'),
		                        
		#                     }
		#                }
		#         )
		# time.sleep(0.5) 
	# print(internal)



	# distance_url = ''
	# adress = ''
	# try:
	# 	if row[0] != 'Provincia code':
	# 		adress = str(row[1]+', '+row[3])
	# 		if row[5] != 'None':
	# 			adress += ', '+row[5]
	# 		try:
	# 			adress += ', '+row[7]
	# 		except Exception as e:
	# 			pass
	# 		try:
	# 			adress += ', '+row[9]
	# 		except Exception as e:
	# 			pass
	# 		point = adress.split(',')
				
	# 		if isNotEmpty(point[-1]):
	# 			it = point[-1]
	# 		else:
	# 			it = point[-2]

	# 		codeIne = getINE(row)
	# 		additional = dumps(coll.find_one({"23_SNIG_CODIGOINE": int(codeIne)}))
	# 		additional_INE = json.loads(additional)
	# 		additional_INE.pop('_id')
	# 		# print (codeIne, point, additional_INE)
	# 		Origin = it
	# 		it = getTitle(it)
	# 		Name_w_Article = it.strip()
	# 		adress = str(row[1]+', '+it)
	# 		# print (it, '<-------------', adress)
	# 		print (adress,  additional_INE['25_SNIG_TIPO'])
	# 		place_id  =  getByPlace(adress, additional_INE['25_SNIG_TIPO'], Name_w_Article)
			
	# 		if place_id:
	# 			gmap = gmap_by_place_id(place_id)
	# 		else:
	# 			gmap = gmap_by_address(adress)

	# 		# gmap['translate'] = getTranslate(adress)
		
			
	# 		print (gmap)
	# 		try:
	# 			if gmap['name'].lower().lstrip().strip() == it.lower().lstrip().strip():
	# 				gmap['comparison'] = True
	# 			else:
	# 				gmap['comparison'] = False
	# 		except Exception as e: 
	# 			gmap['comparison'] = False

	# 		m = hashlib.sha512(str(codeIne).encode('utf-8')).hexdigest()
	# 		gmap['code'] = m
	# 		# wikidata = get_wiki(adress, Name_w_Article, row[1])
	# 		# print (gmap['center'])	
	# 		if 'center' in gmap.keys():

	# 			gmap['15_GMap_center_SNIG_comparison'] = getDistance(gmap['center']['lat'], gmap['center']['lng'],additional_INE['28_SNIG_LATITUD_ETRS89'],additional_INE['29_SNIG_LONGITUD_ETRS89'])
	# 			distance_url =("https://www.google.com.ua/maps/dir/"+str(gmap['center']['lat'])+","+str(gmap['center']['lng'])+"/"+str(additional_INE['28_SNIG_LATITUD_ETRS89'])+","+str(additional_INE['29_SNIG_LONGITUD_ETRS89'])+"")
	# 		wikidata = {}
	# 		internal_obj = make_internal(gmap, row, wikidata, Name_w_Article, additional_INE, distance_url)

	# 	adress = ''
	# 	time.sleep(0.01)
	# 	# print(config.get('googlemaps').get('geocoding').get('key'))
	# except Exception as e:
	# 	print(str(e))

#  AIzaSyDWIGehftKtI7Mi7hPBQ25t-oHn0MY0R2o 

	# gmap_obj.update(gmap)
	# gmap_obj = doc_factory.gmaps()
	# gmap_obj.update(gmap) 
	# if gmap.get('code'):
	# 	gmap_obj = doc_factory.gmaps(gmap.get('code'))
	# 	gmap_obj.update(gmap) 

	# time.sleep(5) 








	# geocode

	# AIzaSyDNdfjGqet-urajuNutvAphLKkdGNPb0tU
	
	# distance
	# AIzaSyDwMgSt7YSWui3RyW9jGbklwakm6ck1AFc
	# AIzaSyAHJ34GoC1EsMfGT5H2N-BmOUbz1XIGKCc

	# placec
	# AIzaSyDhGBybrx1Ir94MmmMpYYgpJASvZS3TVLE
	# AIzaSyAI16xrjPDt9IRmtu8dl5VgxOhZG-hVRrc



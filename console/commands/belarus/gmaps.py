# encoding=utf8
from lib.config.Yaml import Yaml as Config
import pandas as pd
import time
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.spider.Spider import Spider
from lib.parser.map.google.GMapFactory import GMapFactory as MapFactory
from lib.factory.Loader import Loader as LoaderFactory
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


language='ru'
# spider = Spider(
#     loader_factory=LoaderFactory,
#     gmap_parser=MapFactory.spain,
#     wiki_parser=True,
#     doc_factory=doc_factory,
#     language=language,
#     config=config,
#     use_cache=True
# )



def gmap_by_address(address, spider):
    Key = Keygen()
    keyAPI =  Key.get_key_geocode()
    if not keyAPI:
    	sys.exit()
    cnf = {'googlemaps':{'geocoding':{'key': keyAPI}}}
    config.set(cnf)
    spider.gmap_loader._language = language
    objects = spider.get_gmap_address(address)
    gmap = {}
    if objects:
        gmap = objects[0].get_document()

        # gmap.update(language=spider.gmap_loader._language)
    return gmap


for row in db.belarus.find():
	if not 'gmap_name' in row:
		Key = Keygen()
		keyAPI =  Key.get_key_geocode()
		if not keyAPI:
			sys.exit()

		cnf = {'googlemaps':{'geocoding':{'key': keyAPI}}}
		config.set(cnf)
		spider = Spider(
		    loader_factory=LoaderFactory,
		    gmap_parser=MapFactory.spain,
		    wiki_parser=True,
		    doc_factory=doc_factory,
		    language=language,
		    config=config,
		    use_cache=True
		)
		# spider.gmap_loader._language = language

		print('========================================')
		
		
		adress =  str(str(row["NAMEOBJECT"])+' ,'+str(row["NAMESELSOVET"])+' ,'+str(row["NAMEDISTR"]))
		data = gmap_by_address(adress, spider)
		print(data)
		# if 'name' in data:
		# 	print('yessss')
		# 	print(data)
		# else:

		# 	adress =  str(row['DENLOC']+', România')
		# 	data = gmap_by_address(adress, spider)
		# 	print('Nooooooo')
		# 	print(data)
		# print('========================================')
		
		internal = {}

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
		if 'name' in data.keys():
			db.belarus.update_one(
		                {"_id": row['_id'] },
		                    {
		                        "$set": {
		                       	
		                       	'gmap_name': data.get('name'),
		                       	'gmap_admin_hierarchy': data.get('admin_hierarchy', {}),
		                       	'gmap_center': data.get('center'),
		                       	'gmap_bounds': data.get('bounds'),
		                       	'gmap_type': data.get('type'),
		                       	'gmap_translate': data.get('translate'),
		                       	'gmap_requests': data.get('requests'),
		                       	'gmap_code': data.get('code'),
		                       	'gmap_postal_code': data.get('postal_code'),
		                        
		                    }
		               }
		        )
		time.sleep(0.5) 
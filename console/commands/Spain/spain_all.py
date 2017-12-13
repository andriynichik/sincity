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
conn = pymongo.MongoClient('wiki_parser_mongodb', 27017)
db = conn.location
coll = db.SPAININE
config = Config('./config/config.yml')
doc_factory = DocFactory(config.get('mongodb'))
df = pd.read_csv('./data/spain/Spain_notDublicate.csv',  skiprows=18950, low_memory=False)
loader = Loader.loader_with_mongodb(config.get('mongodb'))
headers = {'User-Agent': 'Mozilla/5.0'}
language='es'
spider = Spider(
    loader_factory=LoaderFactory,
    gmap_parser=MapFactory.spain,
    wiki_parser=True,
    doc_factory=doc_factory,
    language=language,
    config=config,
    use_cache=True
)




def gmap_by_address(address):
    objects = spider.get_gmap_address(address)
    gmap = {}
    if objects:
        gmap = objects[0].get_document()
        gmap.update(language=spider.gmap_loader._language)
    return gmap

def gmap_by_place_id(place_id):
    objects = spider.get_gmap_place_id(place_id)
    gmap = {}
    if objects:
        gmap = objects[0].get_document()
        gmap.update(language=spider.gmap_loader._language)
    return gmap

def get_gmap_address_and_components(address, components):
    objects = spider.get_gmap_address_and_components(address, components)
    gmap = {}
    if objects:
        gmap = objects[0].get_document()
        gmap.update(language=spider.gmap_loader._language)
    return gmap

def make_internal(gmap, row, wiki, Name_w_Article, additional_INE, distance_url):
    internal = {}

    if 'name' in gmap.keys():
        internal['10_gmap_name']=gmap.get('name')
    if 'admin_hierarchy' in gmap.keys():
        internal['17_gmap_admin_hierarchy']=gmap.get('admin_hierarchy', {})
    if 'center' in gmap.keys():
        internal['gmap_center']=gmap.get('center')
    if 'bounds' in gmap.keys():
        internal['gmap_bounds']=gmap.get('bounds')

    internal['11_gmap_comparison']=gmap.get('comparison')

    internal['00_INE_Municipio_Code'] = row[2]
    internal['01_INE_Municipio_Name'] = row[3]
    internal['02_INE_Collective_Entity_Code'] = row[4]
    internal['03_INE_Collective_Entity_Name'] = row[5]
    internal['04_INE_Singular_Entity_Code'] = row[6]
    internal['05_INE_Singular_Entity_Name'] = row[7]
    internal['06_INE_Nuclea_Code'] = row[8]
    internal['07_INE_Nuclea_Name'] = row[9]
    internal['08_INE_Name_w_Article'] = Name_w_Article.strip()
    internal['09_INE_Población'] = row[11]
    internal.update(additional_INE)
    internal['15_gmap_comparison_url'] = distance_url
    if 'type' in gmap.keys():
    	internal['12_gmap_type']=gmap.get('type')
    if 'requests' in gmap.keys():
    	internal['13_GMap_requests']=gmap.get('requests')
    if 'name' in wiki.keys():
    	internal.update(wiki_name=gmap.get('name'))
	
    internal['15_GMap_center_SNIG_comparison'] = gmap.get('15_GMap_center_SNIG_comparison')

    if 'admin_hierarchy' in wiki.keys():
        for level in range(1, 12):
        	internal.update(wiki_admin_hierarchy=wiki.get('admin_hierarchy', {}))


    if 'center' in wiki.keys():
        internal.update(wiki_center=wiki.get('center'))
    if 'altitude' in wiki.keys():
        internal.update(wiki_altitude=wiki.get('altitude'))

    if 'population' in wiki.keys():
        internal.update(wiki_population=wiki.get('population'))

    if 'density' in wiki.keys():
        internal.update(wiki_density=wiki.get('density'))
    if 'type' in wiki.keys():
        internal.update(wiki_type=wiki.get('type'))

    if 'url' in wiki.keys():
        internal.update(wiki_url=wiki.get('url'))

    if 'area' in wiki.keys():
        internal.update(wiki_area=wiki.get('area'))

    if 'postal_codes' in wiki.keys():
        internal.update(wiki_postal_codes=wiki.get('postal_codes'))

    internal_obj = doc_factory.internal(gmap['code'])
    internal_obj.update(internal)
    print (internal, gmap['code'])
    return internal_obj

def getByPlace(adress, mytype, Name_w_Article):
	url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?input='+str(adress)+'&types=geocode&language=es&key='+str(config.get('googlemaps').get('geocoding').get('key'))+''
	types = {"Municipio": ["administrative_area_level_4"],
			"Entidad colectiva" :  ["administrative_area_level_5", "neighborhood"],
			"Otras entidades": ["locality", "neighborhood"],
			"Capital de municipio":["locality"],
			"Entidad singular": ["locality"]}
	print(url)
	response = requests.get(url)
	data = response.json()
	print (types[mytype])
	for objects in data['predictions']:
		if objects['types'][0] in types[mytype] :
			if Name_w_Article.lower().lstrip().strip() == objects['structured_formatting']['main_text'].lower().lstrip().strip():			
				print ('############################################################################################################')
				print (objects['place_id'], objects['structured_formatting']['main_text'])
				print ('############################################################################################################')
				return objects['place_id']
	return False

	
def getDistance(lat1,lon1,lat2,lon2):

	url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='+str(lat1)+','+str(lon1)+'&destinations='+str(lat2)+','+str(lon2)+'&key='+str(config.get('googlemaps').get('geocoding').get('key'))+''
	print(url)
	response = requests.get(url)
	data = response.json()
	try:
		resp = data['rows'][0]['elements'][0]['distance']['value'] / 1000
	except Exception as e:
		resp = 0
	
	print (round(resp, 2))
	return round(resp, 2)

def getWikiApi(address):

	url = 'https://es.wikipedia.org/w/api.php?action=query&prop=info|pageimages|coordinates&titles='+str(adress.replace(' ', ''))+'&inprop=url&coprop=type|name|dim|country|region|globe&coprimary=all&rvprop=content&format=json'
	response = requests.get(url)
	data = response.json()
	# print data

def get_wiki(adress, Name_w_Article, provincia):
	url = 'https://es.wikipedia.org/w/index.php?search='+str(adress.replace(' ', ''))+'&title=Sp%C3%A9cial:Recherche&profile=default&fulltext=1&searchengineselect=mediawiki&searchToken=ac9zaxa1lggzxpdhc5ukg06t6'
	
	try:
		content, code = loader.load(url, headers=headers)
		parser = WikiES(content)
		if parser.is_many_answers():
			urls = parser.get_answers_links()
			for answer_url in urls:
				doc = doc_factory.wiki(answer_url)
				page, code = loader.load(answer_url, headers=headers)
				page_parser = WikiES(page)
				data = page_parser.as_dictionary()
				doc = doc_factory.wiki(answer_url)
				data['url'] = answer_url

				if Name_w_Article.lower().lstrip() in data['name'].lower().lstrip():
					if 'admin_hierarchy' in data:
						data['url'] = answer_url
						# print (provincia.lower().lstrip() , data['admin_hierarchy']['ADMIN_LEVEL_3']['name'].lower().lstrip())
						if provincia.lower().lstrip().strip() in data['admin_hierarchy']['ADMIN_LEVEL_3']['name'].lower().lstrip().strip():
							# print ('yessss--->', data['admin_hierarchy']['ADMIN_LEVEL_3']['name'], data)
							return data

	except Exception as e:
		pass
		# print (str(e))
	data = {}
	return data

def isNotEmpty(s):
    return bool(s and s.strip())

def getTitle(point):
	articles = {"(LA)":"La", "(LOS)": "Los", "(O)":"O", "(LAS)":"Las",  "(A)": "A", "(LO)": "Lo", "(EL)":"El"}
	for key, value in articles.items():
		if key in point:
			point = str(value+''+point).replace(key, '').title()
			return point

	return point.title()

def getINE(item):
	if len(str(item[8])) > 10:
		return str(item[8])
	elif len(str(item[6])) > 10:
		return str(item[6])
	elif len(str(item[4])) > 10:
		return str(item[4])
	elif len(str(item[2])) > 10:
		return str(item[2])

for index, row in df.iterrows():
	if index > 995:
		sys.exit()

	Keygen.createGmapsKey('AIzaSyB_jGQLs_V0pHAIkshtQYLr7N-dWuZMd68')
	print (index, Keygen.get_key_geocode())
	distance_url = ''
	adress = ''
	try:
		if row[0] != 'Provincia code':
			adress = str(row[1]+', '+row[3])
			if row[5] != 'None':
				adress += ', '+row[5]
			try:
				adress += ', '+row[7]
			except Exception as e:
				pass
			try:
				adress += ', '+row[9]
			except Exception as e:
				pass
			point = adress.split(',')
				
			if isNotEmpty(point[-1]):
				it = point[-1]
			else:
				it = point[-2]

			codeIne = getINE(row)
			additional = dumps(coll.find_one({"23_SNIG_CODIGOINE": int(codeIne)}))
			additional_INE = json.loads(additional)
			additional_INE.pop('_id')
			Origin = it
			it = getTitle(it)
			Name_w_Article = it.strip()
			adress = str(row[1]+', '+it)
			print (adress,  additional_INE['25_SNIG_TIPO'])
			place_id  =  getByPlace(adress, additional_INE['25_SNIG_TIPO'], Name_w_Article)
			
			if place_id:
				gmap = gmap_by_place_id(place_id)
			else:
				gmap = gmap_by_address(adress)

			print (gmap)
			try:
				if gmap['name'].lower().lstrip().strip() == it.lower().lstrip().strip():
					gmap['comparison'] = True
				else:
					gmap['comparison'] = False
			except Exception as e: 
				gmap['comparison'] = False
			m = hashlib.sha512(str(codeIne).encode('utf-8')).hexdigest()
			gmap['code'] = m
			if 'center' in gmap.keys():
				gmap['15_GMap_center_SNIG_comparison'] = getDistance(gmap['center']['lat'], gmap['center']['lng'],additional_INE['28_SNIG_LATITUD_ETRS89'],additional_INE['29_SNIG_LONGITUD_ETRS89'])
				distance_url =("https://www.google.com.ua/maps/dir/"+str(gmap['center']['lat'])+","+str(gmap['center']['lng'])+"/"+str(additional_INE['28_SNIG_LATITUD_ETRS89'])+","+str(additional_INE['29_SNIG_LONGITUD_ETRS89'])+"")
			wikidata = {}
			internal_obj = make_internal(gmap, row, wikidata, Name_w_Article, additional_INE, distance_url)

		adress = ''
		time.sleep(0.2)
	except Exception as e:
		print(str(e))

#  AIzaSyDWIGehftKtI7Mi7hPBQ25t-oHn0MY0R2o 

	# geocode

	# AIzaSyDNdfjGqet-urajuNutvAphLKkdGNPb0tU
	
	# distance
	# AIzaSyDwMgSt7YSWui3RyW9jGbklwakm6ck1AFc
	# AIzaSyAHJ34GoC1EsMfGT5H2N-BmOUbz1XIGKCc

	# placec
	# AIzaSyDhGBybrx1Ir94MmmMpYYgpJASvZS3TVLE
	# AIzaSyAI16xrjPDt9IRmtu8dl5VgxOhZG-hVRrc



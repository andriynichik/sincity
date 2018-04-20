import csv
from lib.config.Yaml import Yaml as Config
import pandas as pd
import json
import requests
from pymongo import MongoClient
from bson.objectid import ObjectId
import sys
from lib.factory.Loader import Loader as LoaderFactory
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.keygen.gmap_keygen import Keygen
from lib.spider.Spider import Spider
from lib.parser.map.google.GMapFactory import GMapFactory as MapFactory
# from pymongo import Connection
config = Config('./config/config.yml')
mongo_config = config.get('mongodb')
df = pd.read_csv('./data/ukraine/city_UA.csv',  skiprows=0, low_memory=False) 
conn =  MongoClient(mongo_config['host'], mongo_config['port'])
db = conn.location
coll = db.ukraine





def get_place(lat, lng):
    datalist = list()
    url =  'https://maps.googleapis.com/maps/api/place/radarsearch/json?location='+str(lat)+','+str(lng)+'&radius=20000&type=neighborhood&key=AIzaSyAHnEv4kRzWG252YiU9UYIeuqaZrBe_x8M' 
    response = requests.get(url)
    data = response.json()
    result  = data['results']
    # print(data['results'])
    
    for x in result:
        # print (x['place_id'])
        datalist.append(x['place_id'])
        # print ("====================")

    url =  'https://maps.googleapis.com/maps/api/place/radarsearch/json?location='+str(lat)+','+str(lng)+'&radius=20000&type=sublocality&key=AIzaSyAHnEv4kRzWG252YiU9UYIeuqaZrBe_x8M' 
    response = requests.get(url)
    data = response.json()
    result  = data['results']
    # print(data['results'])
    
    for x in result:
        # print (x['place_id'])
        datalist.append(x['place_id'])
        # print ("#########################################")
        
    return datalist

def by_place_id(list_places):
    config = Config('./config/config.yml')
    Key = Keygen()
    keyAPI =  Key.get_key_geocode()
    if not keyAPI:
       sys.exit()

    cnf = {'googlemaps':{'geocoding':{'key': keyAPI}}}
    config.set(cnf)
    language = 'uk'
    doc_factory = DocFactory(config.get('mongodb'))

    spider = Spider(
            loader_factory=LoaderFactory,
            gmap_parser=MapFactory.spain,
            doc_factory=doc_factory,
            language=language,
            config=config,
            use_cache=True
    )
    for loc in list_places:
        objects = spider.get_gmap_place_id(loc)
        gmap = {}
        gmap = objects[0].get_document()
        if :
            pass
        print (gmap)


for index, row in df.iterrows():
    print (row[2], row[3], row[4])
    places = get_place(row[2], row[3])
    print (places)
    by_place_id(places)

    sys.exit()
    # data = {'lat': row[1],
    #         'lng':row[0],
            

    #     }
    # print (data)
    # db.belarus.update_one(
    #                         {"OBJECTNUMBER": row[2]},
    #                             {
    #                                 "$set": {
                                        
    #                                       'lat': row[1],
    #                                       'lng': row[0],
                                        
    #                             }
    #                         }
    #                     )
    # coll.save(data)
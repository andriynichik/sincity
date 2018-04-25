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
coll = db.ukraine_city





def get_place(lat, lng):
    datalist = list()
    
    Key = Keygen()
    keyAPI =  Key.get_key_place()
    if not keyAPI:
       sys.exit()
    url =  'https://maps.googleapis.com/maps/api/place/radarsearch/json?location='+str(lat)+','+str(lng)+'&radius=20000&type=neighborhood&key='+str(keyAPI)+'' 
    response = requests.get(url)
    data = response.json()
    result  = data['results']
    # print(data['results'])
    
    for x in result:
        # print (x['place_id'])
        datalist.append(x['place_id'])
        # print ("====================")

    url =  'https://maps.googleapis.com/maps/api/place/radarsearch/json?location='+str(lat)+','+str(lng)+'&radius=20000&type=sublocality&key='+str(keyAPI)+''
    response = requests.get(url)
    data = response.json()
    result  = data['results']
    # print(data['results'])
    
    for x in result:
        # print (x['place_id'])
        datalist.append(x['place_id'])
        # print ("#########################################")
        
    return datalist

def by_place_id(list_places, city_id):
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
        try:
            gmap = objects[0].get_document()
            gmap["city_id"] = city_id
            exixts = db.ukraine_city_sublocal.find({"city_id": city_id, "code":gmap['code']}).count()
            if exixts < 1:
                gmap.pop('_id', None)
                db.ukraine_city_sublocal.save(gmap)
                print (gmap)

        except Exception as e:
            print (str(e))

for index, row in df.iterrows():
    print (row[2], row[3], row[4])
    places = get_place(row[2], row[3])
    print (places)
    by_place_id(places, row[0])
    data =  {
        "city_id":row[0],
        "region_id":row[1],
        "lat":row[2],
        "lng":row[3],
        "title":row[4],
        "geotype_id":row[5]

    }
    exixts = db.ukraine_city.find({"city_id": data["city_id"]}).count()
    if exixts < 1:
        db.ukraine_city.save(data)
        print ('created',data)
    print(row[0])
  
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
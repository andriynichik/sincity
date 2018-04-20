import csv
from lib.config.Yaml import Yaml as Config
import pandas as pd
import json
import requests
from pymongo import MongoClient
# from pymongo import Connection
config = Config('./config/config.yml')
mongo_config = config.get('mongodb')
df = pd.read_csv('./data/romania/city_RO.csv',  skiprows=0, low_memory=False) 
conn =  MongoClient(mongo_config['host'], mongo_config['port'])
db = conn.location
coll = db.sinoplik_romania
    
for index, row in df.iterrows():
    print(row)

    data = {'sinoptik_id': row[0],
            'region_id':row[1],
            'lat':row[2],
            'lng':row[3],
            'title':row[4],
        }
    print(data)
    coll.save(data)
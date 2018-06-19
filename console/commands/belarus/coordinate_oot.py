import csv
from lib.config.Yaml import Yaml as Config
import pandas as pd
import json
import requests
from pymongo import MongoClient
from bson.objectid import ObjectId

# from pymongo import Connection
config = Config('./config/config.yml')
mongo_config = config.get('mongodb')
df = pd.read_csv('./data/belarus/oopt_wgs84.csv',  skiprows=0, low_memory=False) 
conn =  MongoClient(mongo_config['host'], mongo_config['port'])
db = conn.location
coll = db.belarus_oopt
    
for index, row in df.iterrows():
    print (row)
    # data = {'OBJECTNUMBER': row[0],
    #         'SOATO':row[1],
    #         'NAMEOBJECT':row[2],
    #         'NAME_Type ':row[3],
    #         'NAMEREGION':row[4],
    #         'NAMEDISTR':row[5],

    #     }
    # print (data)
    db.belarus_oopt.update_one(
                            {"OBJECTNUMBER": row[2]},
                                {
                                    "$set": {
                                        
                                          'lat': row[1],
                                          'lng': row[0],
                                        
                                }
                            }
                        )
    # coll.save(data)
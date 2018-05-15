# encoding=utf8

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
df = pd.read_csv('./data/belarus/st_wgs.csv',  skiprows=0, low_memory=False) 
conn =  MongoClient(mongo_config['host'], mongo_config['port'])
db = conn.location
coll = db.belarus_st
    
for index, row in df.iterrows():
    # print (row[2])
    data = {'lat': row[5],
            'lng':row[6],
            

        }
    print (data)
    db.belarus_st.update_one(
                            {"OBJECTNUMBER": int(row[0])},
                                {
                                    "$set": {
                                        
                                          'XCoord': row[5],
                                          'YCoord': row[6],
                                        
                                }
                            }
                        )
    # coll.save(data)
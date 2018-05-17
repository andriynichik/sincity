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
df = pd.read_csv('./data/belarus/bel_st_utf8.csv',  skiprows=0, low_memory=False) 
conn =  MongoClient(mongo_config['host'], mongo_config['port'])
db = conn.location
coll = db.belarus_st
    
for index, row in df.iterrows():
    # print (row[2])
    data = {'NameOblect_C50': row[1],
            'NameSettle_C50':row[4],
            'id':int(float(row[0].replace(',', '.')))
            

        }
    print (data)
    db.belarus_st.update_one(
                            {"OBJECTNUMBER": int(float(row[0].replace(',', '.')))},
                                {
                                    "$set": {
                                        'NameOblect_C50':row[1],
                                        'NameSettle_C50':row[4],
                                        
                                }
                            }
                        )
    # coll.save(data)
# encoding=utf8
import csv
from lib.config.Yaml import Yaml as Config
import pandas as pd
import json
import requests
from pymongo import MongoClient
# from pymongo import Connection
config = Config('./config/config.yml')
mongo_config = config.get('mongodb')
df = pd.read_csv('./data/belarus/st.csv',  skiprows=0, low_memory=False) 
conn =  MongoClient(mongo_config['host'], mongo_config['port'])
db = conn.location
coll = db.belarus_st
    
for index, row in df.iterrows():
    # print (row)
    data = {'OBJECTNUMBER': int(row[0]),
            'NAMEOBJECT':row[1],
            'NAMEOBJECTBELRUS':row[2],
            'Name_Type':row[3],
            'NAMEREGION':row[4],
            'NAMEDISTR':row[5],
            'NAMESELSOVET':row[6],
            
        }
    print (data)
    coll.save(data)
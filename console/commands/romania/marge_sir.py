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
df = pd.read_csv('./data/romania/data.csv',  skiprows=0, low_memory=False) 
conn =  MongoClient(mongo_config['host'], mongo_config['port'])
db = conn.location
coll = db.romania
    
for index, row in df.iterrows():
    data = {'SIRUTA': row[0],
            'DENLOC':row[1],
            'CODP':row[2],
            'JUD':row[3],
            'SIRSUP':row[4],
            'TIP':row[5],
            'NIV':row[6],
            'MED':row[7],
            'REGIUNE':row[8],
            'FSJ':row[9],
            'FS2':row[10],
            'FS3':row[11],
            'FSL':row[12],
            'rang':row[13],


        }
    coll.save(data)
    # print (row[1])


            # 'SNIG_CODIGOINE'
            # 'SNIG_NOMBRE'
            # 'SNIG_COD_PROV'
            # 'SNIG_PROVINCIA'
            # 'SNIG_TIPO'
            # 'SNIG_POBLACION'
            # 'SNIG_INEMUNI'
            # 'SNIG_HOJA_MTN25'
            # 'SNIG_LONGITUD_ETRS89'
            # 'SNIG_LATITUD_ETRS89'
            # 'SNIG_ORIGENCOOR'
            # 'SNIG_ALTITUD'
            # 'SNIG_ORIGENALTITUD'
# encoding=utf8
import csv

import pandas as pd
import json
import requests
import pymongo
# from pymongo import Connection

df = pd.read_csv('./data/spain/ENTIDADES.scv',  skiprows=0, low_memory=False)
conn = pymongo.MongoClient()
conn = pymongo.MongoClient('wiki_parser_mongodb', 27017)
db = conn.location
coll = db.SPAININE


for index, row in df.iterrows():
    data = {'23_SNIG_CODIGOINE': row[0],
            '24_SNIG_NOMBRE':row[1],
            '20_SNIG_COD_PROV':row[2],
            '21_SNIG_PROVINCIA':row[3],
            '25_SNIG_TIPO':row[4],
            '26_SNIG_POBLACION':row[5],
            '22_SNIG_INEMUNI':row[6],
            '30_SNIG_HOJA_MTN25':row[7],
            '29_SNIG_LONGITUD_ETRS89':row[8],
            '28_SNIG_LATITUD_ETRS89':row[9],
            '31_SNIG_ORIGENCOOR':row[10],
            '27_SNIG_ALTITUD':row[11],
            '32_SNIG_ORIGENALTITUD':row[12]

        }
    coll.save(data)
    print (data)


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
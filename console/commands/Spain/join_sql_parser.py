import csv
from lib.config.Yaml import Yaml as Config
import pandas as pd
import json
import requests
from pymongo import MongoClient
from lib.keygen.gmap_keygen import Keygen

# from pymongo import Connection
config = Config('./config/config.yml')
mongo_config = config.get('mongodb')
conn =  MongoClient(mongo_config['host'], mongo_config['port'])
db = conn.location
coll = db.SPAININE

def getDistance(lat1,lon1,lat2,lon2):
    Key = Keygen()
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='+str(lat1)+','+str(lon1)+'&destinations='+str(lat2)+','+str(lon2)+'&key='+str(Key.get_key_distance())+''
    # print(url)
    response = requests.get(url)
    data = response.json()
    try:
        resp = data['rows'][0]['elements'][0]['distance']['value'] / 1000
    except Exception as e:
        resp = 0
    
    print (round(resp, 2))
    return round(resp, 2)

    
for row in db.spain_sql_sinoptik.find():
    
    if 'parser_id' in row:
        
        mod =  db.internal.find_one({"_id": row['parser_id']})
        # print(mod['25_SNIG_TIPO'])
        if mod is not None and  mod['25_SNIG_TIPO'] == 'Municipio': 
           
            parce_data =  db.internal.find_one({"$and": [{"24_SNIG_NOMBRE": row['city_title']}, {"25_SNIG_TIPO": {"$ne": "Municipio"}}]})
            
            if parce_data is not None:
                print(parce_data) 
                # print(row['city_title'])
                # print (parce_data)

                comparison = getDistance(row['lat'], row['lng'], parce_data['28_SNIG_LATITUD_ETRS89'], parce_data['29_SNIG_LONGITUD_ETRS89'])
                comparison_url =("https://www.google.com.ua/maps/dir/"+str(row['lat'])+","+str(row['lng'])+"/"+str(parce_data['28_SNIG_LATITUD_ETRS89'])+","+str(parce_data['29_SNIG_LONGITUD_ETRS89'])+"")
                db.spain_sql_sinoptik.update_one(
                        {"_id": row['_id'] },
                            {
                                "$set": {
                                "parser_id": parce_data['_id'],
                                "comparison": comparison, 
                                "SNIG_NOMBRE": parce_data['24_SNIG_NOMBRE'],
                                "comparison_url":comparison_url,
                                "25_SNIG_TIPO":parce_data['25_SNIG_TIPO'],
                                "status":0,
                                
                            }
                       }
                )
            else:

                db.spain_sql_sinoptik.update_one({"_id" : row['_id'] },{"$unset" : {"status":1, 'parser_id':row['parser_id']}})
                # db.spain_sql_sinoptik.update_one(
                #         {"_id": row['_id'] },
                #             {
                #                 "$set": {
                #                 "parser_id": '',
                #                 "comparison": '#', 
                #                 "SNIG_NOMBRE": '' ,
                #                 "comparison_url": 0,
                #                 "25_SNIG_TIPO":mod['25_SNIG_TIPO'],
                #                 "status":0,
                                
                #             }
                #        }
                # )


    # data = {'23_SNIG_CODIGOINE': row[0],
    #         '24_SNIG_NOMBRE':row[1],
    #         '20_SNIG_COD_PROV':row[2],
    #         '21_SNIG_PROVINCIA':row[3],
    #         '25_SNIG_TIPO':row[4],
    #         '26_SNIG_POBLACION':row[5],
    #         '22_SNIG_INEMUNI':row[6],
    #         '30_SNIG_HOJA_MTN25':row[7],
    #         '29_SNIG_LONGITUD_ETRS89':row[8],
    #         '28_SNIG_LATITUD_ETRS89':row[9],
    #         '31_SNIG_ORIGENCOOR':row[10],
    #         '27_SNIG_ALTITUD':row[11],
    #         '32_SNIG_ORIGENALTITUD':row[12]

    #     }
    # coll.save(data)
    # print (data)
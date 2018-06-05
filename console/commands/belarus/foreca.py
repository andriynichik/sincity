# -*- coding: utf-8 -*-

import csv
from lib.config.Yaml import Yaml as Config
import pandas as pd
import json
import requests
from pymongo import MongoClient
from lib.keygen.gmap_keygen import Keygen
import requests
import sys
from bson.objectid import ObjectId
# from pymongo import Connection
config = Config('./config/config.yml')
mongo_config = config.get('mongodb')
conn =  MongoClient(mongo_config['host'], mongo_config['port'])
db = conn.location




csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_NONE)
myFile = open('foreca.csv', 'w', encoding='utf-8')  

listing_type = [9, 10, 11,17,18,19,22,23,]
with myFile:
    writer = csv.writer(myFile, dialect='myDialect')

    for row in  db.belarus.find():
        if 'sinoptik_db_id' in row :
            data_isset = {  
                        "1410000000":"100630429",
                        "1208510000":"100630279",
                        "1208501000":"100629454",
                        "1401000000":"100629634",
                        "1220501000":"100628884",
                        "1225501000":"100618913",
                        "1230501000":"100627811",
                        "1243501000":"100627145",
                        "1234510000":"100626829",
                        "1252501000":"100625539",
                        "1445000000":"100623549",
                        "1256501000":"100622997",
                        "1258501000":"100621277",
                        "2208501000":"100629640",
                        "2218501000":"100628155",
                        "1258510000":"100629159",
                        "2233510000":"100629055",
                        "2233501000":"100625130",
                        "2418000000":"100624784",
                        "2251501000":"100629400",
                        "3245503000":"100620425",
                        "3208501000":"100620214",
                        "3401000000":"100627907",
                        "3212501000":"100629018",
                        "3216501000":"100618815",
                        "3223501000":"100627751",
                        "3210832026":"100626806",
                        "3235501000":"100625324",
                        "3243501000":"100623581",
                        "3250501000":"100621074",
                        "4208501000":"100620391",
                        "1240505000":"100619818",
                        "4401000000":"100627904",
                        "4236501000":"100626081",
                        "4240501000":"100625367",
                        "4243501000":"100624785",
                        "4249501000":"100630515",
                        "4254501000":"100621754",
                        "5000000000":"100625144",
                        "6208501000":"100630376",
                        "6220501000":"100620445",
                        "6222501000":"100628634",
                        "2221501000":"100629002",
                        "6413000000":"100618800",
                        "6225501000":"100627214",
                        "6234501000":"100625721",
                        "6242501000":"100624700",
                        "2236501000":"100624079",
                        "2238501000":"100623317",
                        "2240501000":"100623760",
                        "2244501000":"100622258",
                        "6246501000":"100621741",
                        "6248501000":"100621729",
                        "6250501000":"100622428",
                        "6252501000":"100621396",
                        "2246501000":"100620833",
                        "7410000000":"100630468",
                        "7220501000":"100627905",
                        "7228501000":"100627202",
                        "7235501000":"100626808",
                        "7240501000":"100626450",
                        "7248501000":"100624034",
                        "7250501000":"100621838",
                        "7254501000":"100629395",
                        "7256501000":"100629347",
                        "7258501000":"100622034",
                    }
        
            if not str(row['SOATO']) in data_isset:
                try:
                    writer.writerows([[row['sinoptik_db_id'], str(row['lat']), str(row['lng']), row['NAMEOBJECT'], row["NAMEREGION"], row["NAMEDISTR"],row["NAMESELSOVET"],row["CENTERATE"],2, 3, 15]])
                except Exception as e:
                    print (str(e))
                        # writer.writerows([[row['29_SNIG_LONGITUD_ETRS89']]])
                        # writer.writerows([[row['28_SNIG_LATITUD_ETRS89']]])
                        # writer.writerows([[row['27_SNIG_ALTITUD']]])
        # if  'sinoptik_db_id' in row:

        #     print('+')
        #     if row['25_SNIG_TIPO'] == 'Municipio' or row['25_SNIG_TIPO'] == 'Entidad colectiva':
        #         print('+!!!!!!!!!!!!!', row['sinoptik_db_id'])
        #         data = {
        #           "event":"Delete",
        #           "id": row['sinoptik_db_id'],
        #         }
        #         r = requests.post('https://55-devsin.ukr.net/admin/api_settle.php', json=data)
        #           # r.json()

        #         respo = r.json()
        #         print (respo)

        #         db.internal.update_one(
        #                       {"_id": row['_id'] },
        #                           {
        #                               "$unset": {
        #                               "sinoptik_db_id":row['sinoptik_db_id'],
        #                               # "status":0,
                                      
        #                           }
        #                      }
       #               )



            # delete {'event': 'Done', 'id': 303668549, 'action': 'created'} 303668559 303668554

        # mod =  db.internal.find_one({"_id": row['parser_id']})
        # # print(mod['25_SNIG_TIPO'])
        # # if mod is not None and  mod['25_SNIG_TIPO'] == 'Municipio': 
           
        # #     parce_data =  db.internal.find_one({"$and": [{"24_SNIG_NOMBRE": row['city_title']}, {"25_SNIG_TIPO": {"$ne": "Municipio"}}]})
            
        # if mod is not None:
        #         # print(parce_data) 
        #         # print(row['city_title'])
        #         # print (parce_data)

        #         # comparison = getDistance(row['lat'], row['lng'], parce_data['28_SNIG_LATITUD_ETRS89'], parce_data['29_SNIG_LONGITUD_ETRS89'])
        #         # comparison_url =("https://www.google.com.ua/maps/dir/"+str(row['lat'])+","+str(row['lng'])+"/"+str(parce_data['28_SNIG_LATITUD_ETRS89'])+","+str(parce_data['29_SNIG_LONGITUD_ETRS89'])+"")
        #     db.spain_sql_sinoptik.update_one(
        #                 {"_id": row['_id'] },
        #                     {
        #                         "$set": {
        #                         # "parser_id": parce_data['_id'],
        #                         # "comparison": comparison, 
        #                         # "SNIG_NOMBRE": parce_data['24_SNIG_NOMBRE'],
        #                         # "comparison_url":comparison_url,
        #                         "25_SNIG_TIPO":mod['25_SNIG_TIPO'],
        #                         # "status":0,
                                
        #                     }
        #                }
        #         )
            # else:

            #     db.spain_sql_sinoptik.update_one({"_id" : row['_id'] },{"$unset" : {"status":1, 'parser_id':row['parser_id']}})
            #     # db.spain_sql_sinoptik.update_one(
            #     #         {"_id": row['_id'] },
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

    #     } scp -r andreynichik:5ktETLJct8Xx@212.42.92.72:/var/www/webcrawler /home 


    # coll.save(data)
    # print (data)
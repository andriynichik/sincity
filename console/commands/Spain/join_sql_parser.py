import csv
from lib.config.Yaml import Yaml as Config
import pandas as pd
import json
import requests
from pymongo import MongoClient
from lib.keygen.gmap_keygen import Keygen
import requests
import sys
# from pymongo import Connection
config = Config('./config/config.yml')
mongo_config = config.get('mongodb')
conn =  MongoClient(mongo_config['host'], mongo_config['port'])
db = conn.location
coll = db.SPAININE


    
for row in  db.internal.find({'17_gmap_admin_hierarchy.ADMIN_LEVEL_1.name': 'España'}):
    
    if not 'sinoptik_db_id' in row:
        try:
            
            if  row['status'] == 4 and row['25_SNIG_TIPO'] != 'Municipio'and row['25_SNIG_TIPO'] != 'Entidad colectiva':
                region = {
                  '1':'1917',
                  '2':'1923',
                  '3':'1910',

                '4':'1911',
                '5':'1916',
                '6':'1924',
                '7':'1915',
                '8':'1909',
                '9':'1916',
                '10':'1924',
                '11':'1911',
                '12':'1910',
                '13':'1923',
                '14':'1911',
                '15':'1918',
                '16':'1923',
                '17':'1909',
                '18':'1911',
                '19':'1923',
                '20':'1917',
                '21':'1911',
                '22':'1912',
                '23':'1911',
                '24':'1916',
                '25':'1909',
                '26':'1922',
                '27':'1918',
                '28':'1908',
                '29':'1911',
                '30':'1913',
                '31':'1920',
                '32':'1918',
                '33':'1919',
                '34':'1916',
                '35':'1914',
                '36':'1918',
                '37':'1916',
                '38':'1914',
                '39':'1921',
                '40':'1916',
                '41':'1911',
                '42':'1916',
                '43':'1909',
                '44':'1912',
                '45':'1923',
                '46':'1910',
                '47':'1916',
                '48':'1917',
                '49':'1916',
                '50':'1912',
                '51':'4734',
                '52':'1925',
            }
            sinoptok_region_id = region[str(row['20_SNIG_COD_PROV'])]
            print(sinoptok_region_id)
            data = {  
                   "event":"Create",
                   "current_sea_id":"0",
                   "lang":"es",
                   "region":"",
                   "settle":row['08_INE_Name_w_Article'],
                   "mod_operation":"1",
                   "district_id":"",
                   "mod_status":"1",
                   "country_id":"186",
                   "region_id":sinoptok_region_id,
                   "geotype_id":"",
                   "parent_id_title":"",
                   "parent_id":"",
                   "parent_id_type":"",
                   "forecast_id_title":"",
                   "forecast_id":"",
                   "forecast_id_type":"",
                   "lat":row['gmap_center']['lat'],
                   "lng":row['gmap_center']['lng'],
                   "altitude":"66",
                   "population":row['09_INE_Población'],
                   "gmt_offset":"",
                   "dst_offset":"",
                   "timezone_id":"336",
                   "is_resort":"0",
                   "mountain_id":"0",
                   "sea_id":"0",
                   "title_ru":"",
                   "old_title_ru":"",
                   "titleIn_ru":"",
                   "old_titleIn_ru":"",
                   "slug_ru":"",
                   "slug_301_ru":"",
                   "title_ua":"",
                   "old_title_ua":"",
                   "titleIn_ua":"",
                   "old_titleIn_ua":"",
                   "slug_ua":"",
                   "slug_301_ua":"",
                   "title_en":"",
                   "old_title_en":"",
                   "titleIn_en":"",
                   "old_titleIn_en":"",
                   "slug_en":"",
                   "slug_301_en":"",
                   "title_pl":"",
                   "old_title_pl":"",
                   "titleIn_pl":"",
                   "old_titleIn_pl":"",
                   "slug_pl":"",
                   "slug_301_pl":"",
                   "title_de":"",
                   "old_title_de":"",
                   "titleIn_de":"",
                   "old_titleIn_de":"",
                   "slug_de":"",
                   "slug_301_de":"",
                   "title_es":"",
                   "old_title_es":"",
                   "titleIn_es":"",
                   "old_titleIn_es":"",
                   "slug_es":"",
                   "slug_301_es":"",
                   "title_fr":"",
                   "old_title_fr":"",
                   "titleIn_fr":"",
                   "old_titleIn_fr":"",
                   "slug_fr":"",
                   "slug_301_fr":"",
                   "title_pt":"",
                   "old_title_pt":"",
                   "titleIn_pt":"",
                   "old_titleIn_pt":"",
                   "slug_pt":"",
                   "slug_301_pt":"",
                   "title_it":"",
                   "old_title_it":"",
                   "titleIn_it":"",
                   "old_titleIn_it":"",
                   "slug_it":"",
                   "slug_301_it":"",
                   "title_nl":"",
                   "old_title_nl":"",
                   "titleIn_nl":"",
                   "old_titleIn_nl":"",
                   "slug_nl":"",
                   "slug_301_nl":"",
                   "title_da":"",
                   "old_title_da":"",
                   "titleIn_da":"",
                   "old_titleIn_da":"",
                   "slug_da":"",
                   "slug_301_da":"",
                   "title_no":"",
                   "old_title_no":"",
                   "titleIn_no":"",
                   "old_titleIn_no":"",
                   "slug_no":"",
                   "slug_301_no":"",
                   "title_cs":"",
                   "old_title_cs":"",
                   "titleIn_cs":"",
                   "old_titleIn_cs":"",
                   "slug_cs":"",
                   "slug_301_cs":"",
                   "title_bg":"",
                   "old_title_bg":"",
                   "titleIn_bg":"",
                   "old_titleIn_bg":"",
                   "slug_bg":"",
                   "slug_301_bg":"",
                   "title_hu":"",
                   "old_title_hu":"",
                   "titleIn_hu":"",
                   "old_titleIn_hu":"",
                   "slug_hu":"",
                   "slug_301_hu":"",
                   "title_sk":"",
                   "old_title_sk":"",
                   "titleIn_sk":"",
                   "old_titleIn_sk":"",
                   "slug_sk":"",
                   "slug_301_sk":"",
                   "title_sl":"",
                   "old_title_sl":"",
                   "titleIn_sl":"",
                   "old_titleIn_sl":"",
                   "slug_sl":"",
                   "slug_301_sl":"",
                   "title_sh":"",
                   "old_title_sh":"",
                   "titleIn_sh":"",
                   "old_titleIn_sh":"",
                   "slug_sh":"",
                   "slug_301_sh":"",
                   "title_hr":"",
                   "old_title_hr":"",
                   "titleIn_hr":"",
                   "old_titleIn_hr":"",
                   "slug_hr":"",
                   "slug_301_hr":"",
                   "version_ua":"1",
                   "version_ru":"1",
                   "version_gb":"1",
                   "accepted":"1"
                }
            print (row)
            r = requests.post('https://55-devsin.ukr.net/admin/api_settle.php', json=data)
                # r.json()
            respo = r.json()
            print (respo['id'])

            db.internal.update_one(
                            {"_id": row['_id'] },
                                {
                                    "$set": {
                                    "sinoptik_db_id":respo['id'],
                                    # "status":0,
                                    
                                }
                           }
                    )
        except Exception as e:
                print (str(e))
 
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

    #     }
    # coll.save(data)
    # print (data)
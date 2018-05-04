import csv
from lib.config.Yaml import Yaml as Config
import pandas as pd
import json
import requests
from pymongo import MongoClient
from bson.objectid import ObjectId
from lib.keygen.gmap_keygen import Keygen
import requests
import sys
# from pymongo import Connection
config = Config('./config/config.yml')
mongo_config = config.get('mongodb')
conn =  MongoClient(mongo_config['host'], mongo_config['port'])
db = conn.location
coll = db.SPAININE
listing_type = [9, 10, 11,17,18,19,22,23,]
for row in db.romania.find():
    
    if not 'sinoptik_db_id' in row :
        count  =  db.sinoplik_romania.find({'parser_id':  ObjectId(row['_id'])}).count()
        if count > 0:
            
            md  =  db.sinoplik_romania.find_one({'parser_id':  ObjectId(row['_id'])})
            db.romania.update_one(
                                  {"_id": row['_id'] },
                                      {
                                          "$set": {
                                          "sinoptik_db_id":md['sinoptik_id'],
                                          # "status":0,
                                          
                                      }
                                 }
                          )
            print(md['sinoptik_id'])
        else:
            try:
                if row['TIP'] in listing_type:
                    
                    region = {
                            "23":"2502",
                            "40":"2460",
                            "1":"2495",
                            "8":"2466",
                            "14":"2497",
                            "26":"2475",
                            "32":"2474",
                            "19":"2501",
                            "4":"2471",
                            "7":"2478",
                            "37":"2491",
                            "27":"2483",
                            "33":"2481",
                            "22":"2467",
                            "6":"2488",
                            "5":"2470",
                            "12":"2461",
                            "24":"2476",
                            "30":"2479",
                            "31":"2496",
                            "3":"2473",
                            "52":"2494",
                            "15":"2487",
                            "51":"2492",
                            "29":"2468",
                            "34":"2500",
                            "21":"2499",
                            "9":"2469",
                            "10":"2477",
                            "39":"2482",
                            "17":"2465",
                            "":"2498",
                            "13":"2464",
                            "36":"2486",
                            "38":"2480",
                            "18":"2485",
                            "16":"2463",
                            "25":"2484",
                            "28":"2490",
                            "2":"2472",
                            "11":"2489",
                            "35":"2462",
                            "20":"2493",
                      }
                    sinoptok_region_id = region[str(row['JUD'])]
                    print(sinoptok_region_id)
                    data = {  
                             "event":"Create",
                             "current_sea_id":"0",
                             "lang":"ro",
                             "region":"",
                             "settle":row['DENLOC'],
                             "mod_operation":"1",
                             "district_id":"",
                             "mod_status":"1",
                             "country_id":"164",
                             "region_id":sinoptok_region_id,
                             "geotype_id":"",
                             "parent_id_title":"",
                             "parent_id":"",
                             "parent_id_type":"",
                             "forecast_id_title":"",
                             "forecast_id":"",
                             "forecast_id_type":"",
                             "lat":row['wiki_center'],
                             "lng":row['wiki_center'],
                             "altitude":"",
                             "population":"",
                             "gmt_offset":"",
                             "dst_offset":"",
                             "timezone_id":"319",
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

                    db.romania.update_one(
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
 

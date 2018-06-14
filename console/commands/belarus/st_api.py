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
for row in db.belarus_st.find({}, no_cursor_timeout=True):
    
    if not 'sinoptik_db_id' in row :
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
        
    
        try:
        
 
            if 'status_center' in row:
                if 'XCoord' in row and 'YCoord' in row:
                        
                    
                    region = {
                                "Брестская":"1793",
                                "Витебская":   "1797",
                                "Гомельская":  "1791",
                                "Гродненская": "1792",
                                "Минская": "1795",
                                "Могилевская": "1794",
                                "Минск":"1790"

                          }


                    sinoptok_region_id = region[str(row['NAMEREGION'])]
                    print(sinoptok_region_id)
                    data = {  
                                 "event":"Create",
                                 "current_sea_id":"0",
                                 "lang":"ro",
                                 "region":"",
                                 "settle":row['NAMEOBJECT'],
                                 "mod_operation":"1",
                                 "district_id":"",
                                 "mod_status":"1",
                                 "country_id":"18",
                                 "region_id":sinoptok_region_id,
                                 "geotype_id":"",
                                 "parent_id_title":"",
                                 "parent_id":"",
                                 "parent_id_type":"",
                                 "forecast_id_title":"",
                                 "forecast_id":"",
                                 "forecast_id_type":"",
                                 "lat":str(row['XCoord']),
                                 "lng":str(row['YCoord']),
                                 "altitude":"",
                                 "population":"",
                                 "gmt_offset":"2",
                                 "dst_offset":"3",
                                 "timezone_id":"339",
                                 "is_resort":"0",
                                 "mountain_id":"0",
                                 "sea_id":"0",
                                 "title_ru":row['NAMEOBJECT'],
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
                                 "version_ua":"0",
                                 "version_ru":"0",
                                 "version_gb":"0",
                                 "accepted":"1"
                              }
                    print (data)
                    r = requests.post('https://55-devsin.ukr.net/admin/api_settle.php', json=data)
                              # r.json()
                    respo = r.json()
                    print (respo)

                    db.belarus_st.update_one(
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
 

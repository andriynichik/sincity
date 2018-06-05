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

list_re = [ 304122759

                , 304122834

                , 304122619

                , 304122914

                , 304122624

                , 304122919

                , 304122714

                , 304122629

                , 304122764

                , 304122769

                , 304122634

                , 304122839

                , 304122774

                , 304122924

                , 304122609

                , 304122719

                , 304122639

                , 304122929

                , 304122934

                , 304122939

                , 304122644

                , 304122844

                , 304122849

                , 304122944

                , 304122779

                , 304122784

                , 304122949

                , 304122649

                , 304122724

                , 304122654

                , 304122854

                , 304122659

                , 304122664

                , 304122729

                , 304122859

                , 304122864

                , 304122734

                , 304122789

                , 304122869

                , 304122739

                , 304122669

                , 304122674

                , 304122874

                , 304122794

                , 304122679

                , 304122954

                , 304122879

                , 304122799

                , 304122884

                , 304122684

                , 304122744

                , 304122889

                , 304122804

                , 304122689

                , 304122959

                , 304122694

                , 304122699

                , 304122809

                , 304122814

                , 304122749

                , 304122819

                , 304122964

                , 304122969

                , 304122894

                , 304122899

                , 304122904

                , 304122974

                , 304122979

                , 304122704

                , 304122984

                , 304122989

                , 304122824

                , 304122829

                , 304122754

                , 304122709]

for row in db.belarus.find({}, no_cursor_timeout=True):
    
    if 'sinoptik_db_id' in row and  row['sinoptik_db_id'] in list_re :
        region = {
                                "Брестская":"1793",
                                "Витебская":   "1797",
                                "Гомельская":  "1791",
                                "Гродненская": "1792",
                                "Минская": "1795",
                                "Могилевская": "1794",
                                "Минск":"1790"

                          }


        sinoptok_region_id = region[str(row['NAMEDISTR'])]
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
                                 "lat":str(row['lat']),
                                 "lng":str(row['lng']),
                                 "altitude":"",
                                 "population":"",
                                 "gmt_offset":"",
                                 "dst_offset":"",
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
        print (respo['id'])

        db.belarus.update_one(
                                          {"_id": row['_id'] },
                                              {
                                                  "$set": {
                                                  "sinoptik_db_id":respo['id'],
                                                  # "status":0,
                                                  
                                              }
                                         }
                                  )
             

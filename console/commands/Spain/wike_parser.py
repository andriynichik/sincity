import csv
from lib.config.Yaml import Yaml as Config
import pandas as pd
import time
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.spider.Spider import Spider
from lib.parser.map.google.GMapFactory import GMapFactory as MapFactory
from lib.factory.Loader import Loader 
import math
import wikipedia
import datetime
import sys
from lib.parser.wiki.Spain import Spain as WikiES
from lib.logger.File import File as FileLog
from argparse import ArgumentParser

# from lib.parser.wiki.Spain import Spain as ParserSpain
country = 'Spain'

config = Config('./config/config.yml')
document_factory = DocFactory(config.get('mongodb'))
df = pd.read_csv('./data/spain/Spain_notDublicate.csv',  skiprows=[1])
# print(config)
language='es'
# spider = Spider(
#     loader_factory=LoaderFactory,
#     gmap_parser=MapFactory.spain,
#     wiki_parser=True,
#     doc_factory=doc_factory,
#     language=language,
#     config=config,
#     use_cache=True
# )
loader = Loader.loader_with_mongodb(config.get('mongodb'))
def gmap_by_address(address):
    objects = spider.get_gmap_address(address)
    gmap = {}
    if objects:
        gmap = objects[0].get_document()
        gmap.update(language=spider.gmap_loader._language)
    return gmap


# print (wikipedia.search("Coruña"))
headers = {'User-Agent': 'Mozilla/5.0'}
for index, row in df.iterrows():
    # print (str(row[3])+','+str(row[5])+','+str(row[7])+','+str(row[9]))


    try:
        # if not math.isnan(str(row[9])):
        #     print (str(row[9]))

        if row[0] != 'Provincia code':
            adress = str(row[1]+' , '+row[3])
            if row[5] != 'None':
                adress += ' , '+row[5]
            try:
                adress += ' , '+row[7]
            except Exception as e:
                pass
            try:
                adress += ' , '+row[9]
            except Exception as e:
                pass
            point = adress.split(',')
            url = 'https://es.wikipedia.org/w/index.php?search='+str(adress.replace(' ', ''))+'&title=Sp%C3%A9cial:Recherche&profile=default&fulltext=1&searchengineselect=mediawiki&searchToken=ac9zaxa1lggzxpdhc5ukg06t6'
        # adress = str(row[1]+' , '+row[3])
            content, code = loader.load(url, headers=headers)
            parser = WikiES(content)
            print (adress, '=====================================================================================', url)
            # print (url) (LA) (LAS) (EL)
    
            if parser.is_many_answers():
                urls = parser.get_answers_links()
                for answer_url in urls:
                    print (answer_url)
                    doc = document_factory.wiki(answer_url)
                    page, code = loader.load(answer_url, headers=headers)
                    page_parser = WikiES(page)
                        # print (code)
                        # print(page_parser.as_dictionary())
                    data = page_parser.as_dictionary()
                    print(data['name'])
                    doc = document_factory.wiki(answer_url)
                    if point[-1].lower().lstrip().replace('(LA)', '').replace('(LAS)', '').replace('(EL)', '') in data['name'].lower().lstrip():
                        print (data, 'YEEEESSSS')
                        data['Municipio_Name'] = row[3]
                        data['Collective_Entity_Code'] = row[4]
                        data['Collective_Entity_Name'] = row[5]
                        data['Singular_Entity_Code'] = row[6]
                        data['Singular_Entity_Name'] = row[7]
                        data['Nuclea_Code'] = row[8]
                        data['Nuclea_Name'] = row[9]
                        doc.update(data)
                    # if page_parser.is_location_page():
                    #     print(page_parser.as_dictionary())
            elif parser.is_location_page():
                 print('is_location_page')

            time.sleep(1)
        # url = 'https://es.wikipedia.org/w/index.php?search=Almería,LUBRÍN , RAMBLA ALJIBE (LA)&title=Sp%C3%A9cial:Recherche&profile=default&fulltext=1&searchengineselect=mediawiki&searchToken=ac9zaxa1lggzxpdhc5ukg06t6'
        # adress = str(row[1]+' , '+row[3])
        # if row[5] != 'None':
        #     adress = row[5]
        # try:
        #     if not math.isnan(row[7]):
        #         adress = row[7]
            
        # except Exception as e:
        #     print(str(e))
        # try:
        #     print (row[9])
        #     if not math.isnan(row[9]):
        #         adress = row[9]
        # except Exception as e:
        #     print(str(e))

        # gmap = gmap_by_address(adress.encode('utf-8'))
        # print (adress)
        # gmap_obj = doc_factory.gmaps(gmap.get('code'))
        # gmap_obj.update(gmap)
        # print (gmap) 
    except Exception as e:
        print(str(e))

#  AIzaSyDWIGehftKtI7Mi7hPBQ25t-oHn0MY0R2o 

    # gmap_obj.update(gmap)
    # gmap_obj = doc_factory.gmaps()
    # gmap_obj.update(gmap) 
    # if gmap.get('code'):
    #   gmap_obj = doc_factory.gmaps(gmap.get('code'))
    #   gmap_obj.update(gmap) 

    # time.sleep(5) 
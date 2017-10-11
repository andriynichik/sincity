from DataStructure.DataWiki import parser_wiki
from DataStructure.DataGMap import parser_gmap
from DataStructure.DataInsee import parser_insee
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.config.Yaml import Yaml as Config


import csv

files = [
    'DataStructure/20_08_17_canton_google_3.csv',
    'DataStructure/arrondissements_25_08_17_cards.csv',
    'DataStructure/Departements_28_08_17_cards.csv',
    'DataStructure/communes_17_09_17.csv'
]

config = Config('./config/config.yml')

doc_factory = DocFactory(config.get('mongodb'))

for csv_file in files:
    with open(csv_file, encoding='utf-8') as admin_div_CSV:
        for line in csv.DictReader(admin_div_CSV, delimiter='\t'):

            dct = {}

            wiki = parser_wiki(line)

            gmap = parser_gmap(line)

            insee = parser_insee(line)





            print(wiki)
            print(gmap)
            print(insee)
            break

            wiki_obj = doc_factory.wiki(wiki.get('url'))
            wiki_obj.update(wiki)

            gmap_obj = doc_factory.gmaps(gmap.get('code'))
            gmap_obj.update(gmap)

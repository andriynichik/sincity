from DataStructure.DataWiki import parser_wiki
from DataStructure.DataGMap import parser_gmap

import csv

# csv_file = '20_08_17_canton_google_3.csv'
# csv_file = 'arrondissements_25_08_17_cards.csv'
# csv_file = 'Departements_28_08_17_cards.csv'
csv_file = 'communes_17_09_17.csv'

n=0
with open(csv_file, encoding='utf-8') as cantonCSV:
    for line in csv.DictReader(cantonCSV, delimiter='\t'):

        n += 1

        dct = {}

        wiki = parser_wiki(line)
        gmap = parser_gmap(line)

        dct.update({'wiki': wiki})
        dct.update({'gmap': gmap})

        print(dct)

        # if n>= 2:
        #     break
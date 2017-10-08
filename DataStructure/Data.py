from DataStructure.DataWiki import parser_wiki
from DataStructure.DataGMap import parser_gmap

import csv

# csv_file = '20_08_17_canton_google_3.csv'
# csv_file = 'arrondissements_25_08_17_cards.csv'
# csv_file = 'Departements_28_08_17_cards.csv'
csv_file = 'communes_17_09_17.csv'

name_file_txt = csv_file.replace('.csv', '.txt')
with open(name_file_txt, 'w') as dt_file:
    with open(csv_file, encoding='utf-8') as admin_div_CSV:
        for line in csv.DictReader(admin_div_CSV, delimiter='\t'):

            dct = {}

            wiki = parser_wiki(line)
            gmap = parser_gmap(line)

            dct.update({'wiki': wiki})
            dct.update({'gmap': gmap})

            dt_file.writelines(str(dct) + '\n')

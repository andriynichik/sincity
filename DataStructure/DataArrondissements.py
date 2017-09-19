from lib.hashlib.sha512 import sha512 as hash
import csv
import re

url = 'https://fr.wikipedia.org'

with open('arrondissements_25_08_17_cards.csv', encoding='utf-8') as csvfile:
    for line in csv.DictReader(csvfile, delimiter='\t'):


        name_pays = line.get('W_Pays')
        name_region = line.get('W_Region')
        name_departement = line.get('W_Departement')
        name_arrondissement = line.get('I_Nccent')

        admin_hierarchy = [
            {'name': name_pays, 'type': 'ADMIN_LEVEL_1'},
            {'name': name_region, 'type': 'ADMIN_LEVEL_2'},
            {'name': name_departement, 'type': 'ADMIN_LEVEL_3'},
            {'name': name_arrondissement, 'type': 'ADMIN_LEVEL_4'},
        ]

        in_18 = {}
        for key, val in line.items():
            if re.match(r'^(W_Name_){1}[a-z]{2}', key):
                if line.get(key):
                    in_18[key[-2:]] = val
### wiki
        wiki_url = line.get('Wiki_Url')

        code = hash().make([name_arrondissement, url + wiki_url])

        code_arrondissements = line.get('I_Code_Arrondissements')
        req = (
            'https://fr.wikipedia.org/w/index.php?search="code+arrondissement+{}"'.format(code_arrondissements)
        )

        print(req)


        break
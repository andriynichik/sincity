from lib.hashlib.sha512 import sha512 as hash
import csv
import re

wiki_france = 'https://fr.wikipedia.org/'


def get_url(row):
    try:
        url = row['Wiki_Url']
    except KeyError:
        return None
    return url


def different_languages(row):
    in_18 = {}
    for key, val in row.items():
        if re.match(r'^(W_Name_){1}[a-z]{2}', key):
            if row.get(key):
                country = key[-2:]
                url_lang = row.get('W_Url_{}'.format(country))
                in_18[country] = {'name': val}
                if url_lang:
                    in_18.update({country: {'url': url_lang}})
    return in_18


with open('arrondissements_25_08_17_cards.csv', encoding='utf-8') as csvfile:
    for line in csv.DictReader(csvfile, delimiter='\t'):

        dct = {
            'wiki': {},
            'gmap': {},
            'other': {},
        }


        name_pays = line.get('W_Pays')
        name_region = line.get('W_Region')
        name_departement = line.get('W_Departement')
        name_arrondissement = line.get('Wiki_name_arrondissement')

        admin_hierarchy = [
            {'name': name_pays, 'type': 'ADMIN_LEVEL_1'},
            {'name': name_region, 'type': 'ADMIN_LEVEL_2'},
            {'name': name_departement, 'type': 'ADMIN_LEVEL_3'},
            {'name': name_arrondissement, 'type': 'ADMIN_LEVEL_4'},
        ]

        in_18 = different_languages(line)

        dct['wiki'].update({'in_18': in_18})
        dct['wiki'].update({'name': name_arrondissement})

        for admin_division in admin_hierarchy:
            if admin_division['name'] == dct['wiki']['name']:
                dct['wiki'].update({'type': admin_division['type']})

### wiki
        wiki_url = get_url(line)
        if wiki_url:
            url = wiki_france + wiki_url
            code = hash().make([url])
            dct['wiki'].update({'url': url})
            dct['wiki'].update({'code': code})



        code_arrondissements = line.get('I_Code_Arrondissements')
        req = (
            'https://fr.wikipedia.org/w/index.php?search="code+arrondissement+{}"'.format(code_arrondissements)
        )

        print(dct)


        break
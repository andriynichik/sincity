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


def admin_division(row, wiki_admin):
    admin_hierarchy = []
    n = 0
    for admin_div in wiki_admin:
        n += 1
        name = row.get(admin_div)
        if name:
            admin_hierarchy.append({'name': name, 'type': 'ADMIN_LEVEL_{}'.format(n)})
    return admin_hierarchy


with open('arrondissements_25_08_17_cards.csv', encoding='utf-8') as csvfile:
    for line in csv.DictReader(csvfile, delimiter='\t'):

        dct = {
            'wiki': {},
            'gmap': {},
            'other': {},
        }


        wiki_name_admins_keys = ['W_Pays',
                                 'W_Region',
                                 'W_Departement',
                                 'Wiki_name_arrondissement',
        ]

        admin_hierarchy = admin_division(line, wiki_name_admins_keys)

        in_18 = different_languages(line)

        dct['wiki'].update({'in_18': in_18})

        name_arrondissement = line.get(wiki_name_admins_keys[-1])
        if name_arrondissement:
            dct['wiki'].update({'name': name_arrondissement})
            for ad in admin_hierarchy:
                if ad['name'] == dct['wiki']['name']:
                    dct['wiki'].update({'type': ad['type']})

        wiki_url = get_url(line)
        if wiki_url:
            url = wiki_france + wiki_url
            code = hash().make([url])
            dct['wiki'].update({'url': url})
            dct['wiki'].update({'code': code})

        capital = line.get('W_Chef-lieu')
        if capital:
            dct['wiki'].update({'capital': capital})

        lat = line.get('Wiki_Coordinates_lat')
        lon = line.get('Wiki_Coordinates_lon')
        if lat is not None and lon is not None:
            dct['wiki'].update({'center': {
                                            'lat': float(lat),
                                            'lon': float(lon),
                                          }
                               })



        # code_arrondissements = line.get('I_Code_Arrondissements')
        # req = (
        #     'https://fr.wikipedia.org/w/index.php?search="code+arrondissement+{}"'.format(code_arrondissements)
        # )

        print(dct)


        break
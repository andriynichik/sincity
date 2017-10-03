from lib.hashlib.sha512 import sha512 as hash
import re

wiki_res = {}
wiki_france = 'https://fr.wikipedia.org'


def parser_wiki(line):
    wiki_res = {}
    # wiki_res.update(get_name(line))
    # wiki_res.update(different_languages(line))
    # wiki_res.update(get_url(line))
    wiki_res.update(get_population(line))
    # wiki_res.update(get_density(line))
    # wiki_res.update(get_area(line))
    # wiki_res.update(get_coordinates(line))
    # wiki_res.update(hierarchy(line))
    # wiki_res.update(get_capital(line))
    # wiki_res.update({'other': line})
    return wiki_res

def get_name(row):
    try:
        name_admin = {'name': row['Wiki_Name_Snipet']}
    except KeyError:
        return {}
    return name_admin


def different_languages(row):
    i18n = {}
    for key, val in row.items():
        if re.match(r'^(W_Name_){1}[a-z]{2}', key):
            if row.get(key):
                country = key[-2:]
                url_lang = row.get('W_Url_{}'.format(country))
                i18n[country] = {'name': val}
                if url_lang != None:
                    i18n.update({country: {'url': url_lang}})
    if i18n:
        return {'i18n': i18n}
    return {}


def get_url(row):
    try:
        url = row['Wiki_Url']
    except KeyError:
        return {}
    if url != 'None':
        url = wiki_france + url
        code = hash().make(url)
        return {'url': url, 'code': code}
    return {}


def get_population(row):
    try:
        population_string = row['W_Population']
    except KeyError:
        return {}
    if population_string != 'None':
        population = get_number(' hab.', population_string)
        return {'population': int(population)} # TODO в департаментах одно поле не читается нужно разобраться
    return {}


def get_density(row):
    try:
        density_string = row['W_Densite']
    except KeyError:
        return {}
    if density_string != 'None':
        density = get_number(' hab./km2', density_string)
        return {'density': density}
    return {}


def get_area(row):
    try:
        area_string = row['W_Superficie']
    except KeyError:
        return {}
    if area_string != 'None':
        area = get_number(' km2', area_string)
        return {'area': area}
    return {}


def get_number(identificator, number):
    pat = r'([\d\s,]*)(?={})'.format(identificator)
    result = re.match(pat, number)
    if result == None:
        return 0
    result = re.sub('\s', '', result.group())
    if ',' in result:
        result = result.replace(',', '.')
    return float(result)


def get_coordinates(row):
    try:
        lat = row['Wiki_Coordinates_lat']
        lon = row['Wiki_Coordinates_lon']
    except KeyError:
        return {}
    if lat != 'None' and lon != 'None':
        coordinates = {'center': {
                                  'lat': float(lat),
                                  'lon': float(lon),
                                 }
                      }
        return coordinates
    return {}

def hierarchy(row):
    hierarchy_list = [
        'W_Pays',
        'W_Region',
        'W_Departement',
        'W_Arrondissement',
        'W_Canton',
        'W_Intercommunalite',
        'W_Commune',
    ]
    level = 0
    res_hierarchy = []
    for admin_div in hierarchy_list:
        try:
           admin_unit = row[admin_div]
        except KeyError:
            level += 1
            res_hierarchy.append({'name': row['Wiki_Name_Snipet'], 'type': 'ADMIN_LEVEL_{}'.format(level)})
            return dict(admin_hierarchy=res_hierarchy)
        if admin_unit != 'None':
            level += 1
            res_hierarchy.append({'name': admin_unit, 'type': 'ADMIN_LEVEL_{}'.format(level)})

    return dict(admin_hierarchy=res_hierarchy)


def get_capital(row):
    try:
        try:
            capital = row['W_Chef_lieu']
        except KeyError:
            capital = row['W_Chef-lieu']
    except KeyError:
        return {}
    if capital != 'None':
        return {'capital': capital}
    return {}

from lib.hashlib.sha512 import sha512 as hash
import re


wiki_france = 'https://fr.wikipedia.org'


def parser_wiki(line):
    wiki_res = {}

    functions_parser = (
        get_name,
        different_languages,
        get_url,
        get_population,
        get_density,
        get_area,
        get_coordinates,
        hierarchy,
        get_capital,
        get_postal_code,
        get_altitude,
        get_other,
    )

    for func in functions_parser:
        wiki_res.update(func(line))

    return wiki_res


def get_name(row):
    try:
        try:
            name_admin = {'name': row['Wiki_Name_Snipet']}
        except KeyError:
            name_admin = {'name': row['Wiki_NameSnipet']}
    except KeyError:
        return {}
    return name_admin


def different_languages(row):
    i18n = {}
    for key, val in row.items():
        if re.match(r'^(W_Name_)[a-z]{2}', key):
            if row.get(key):
                country = key[-2:]
                url_lang = row.get('W_Url_{}'.format(country))
                i18n[country] = {'name': val}
                if url_lang is not None:
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
    if population_string not in ['None', '']:
        population = get_number(' hab.', population_string)
        if isinstance(population, float):
            return {'population': int(population)}
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
    result = re.search(pat, number)
    if result is None:
        return {}
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
            try:
                name = row['Wiki_Name_Snipet']
            except KeyError:
                name = row['Wiki_NameSnipet']
            res_hierarchy.append({'name': name, 'type': 'ADMIN_LEVEL_{}'.format(level)})
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


def get_postal_code(row):
    try:
        postal_code = row['W_CodePostal']
    except KeyError:
        return {}
    if postal_code != 'None':
        return {'postal_code': (postal_code,)}
    return {}


def get_altitude(row):
    try:
        altitude = row['W_Altitude']
    except KeyError:
        return {}
    if altitude != 'None':
        return {'altitude': altitude}
    return {}


def get_other(row):
    other = {'other': {}}
    other_wiki = [
        'W_Bureau',
        'W_Cordommees',
        'W_Creation',
    ]
    for name_column in other_wiki:
        try:
            value = row[name_column]
        except KeyError:
            continue
        if value not in ['', 'None']:
            var = name_column[2:].lower()
            other['other'].update({var: value})
    return other

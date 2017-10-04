def parser_gmap(line):
    gmap_res = {}
    gmap_res.update(long_name(line))
    gmap_res.update(short_name(line))
    gmap_res.update(get_code(line))
    gmap_res.update(get_type(line))
    return gmap_res


def long_name(row):
    try:
        name = row['G_Country_long_name']
    except KeyError:
        return {}
    if name not in ['None', '']:
        return {'long_name': name}
    return {}


def short_name(row):
    try:
        name = row['G_Country_short_name']
    except KeyError:
        return {}
    if name not in ['None', '']:
        return {'short_name': name}
    return {}


def get_code(row):
    try:
        gpi = row['G_PlaceId']
    except KeyError:
        return {}
    if gpi not in ['None', '']:
        return {'code': gpi}
    return {}


def get_type(row):
    try:
        types = row['G_Types']
    except KeyError:
        return {}
    if types not in ['None', '']:
        return {'type': types}
    return {}

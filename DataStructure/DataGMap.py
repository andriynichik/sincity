def parser_gmap(line):
    gmap_res = {}
    gmap_res.update(long_name(line))
    gmap_res.update(short_name(line))
    return gmap_res

def long_name(row):
    try:
        name = row['G_Locality_long_name']
    except KeyError:
        return {}
    if name not in ['None', '']:
        return {'long_name': name}
    return {}

def short_name(row):
    try:
        name = row['G_Locality_short_name']
    except KeyError:
        return {}
    if name not in ['None', '']:
        return {'short_name': name}
    return {}
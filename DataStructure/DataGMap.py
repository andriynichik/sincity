def parser_gmap(line):
    gmap_res = {}

    data_parser = (
        ('G_Locality_long_name', 'long_name'),
        ('G_Locality_short_name', 'short_name'),
        ('G_PlaceId', 'code'),
        ('G_Types', 'type')
        ('G_FormatAddress', 'address'),
        ('G_postal_code_long_name', 'postal_code'),
    )

    for value in data_parser:
        gmap_res.update(pars(line, value[0], value[1]))

    functions_parser = (
        get_center,
        get_bounds,
    )

    for func in functions_parser:
        gmap_res.update(func(line))

    return gmap_res


def pars(row, column_name, res_name):
    try:
        name = row[column_name]
    except KeyError:
        return {}
    if name not in ['None', '']:
        return {res_name: name}
    return {}
#
# def long_name(row):
#     try:
#         name = row['G_Country_long_name']
#     except KeyError:
#         return {}
#     if name not in ['None', '']:
#         return {'long_name': name}
#     return {}
#
#
# def short_name(row):
#     try:
#         name = row['G_Country_short_name']
#     except KeyError:
#         return {}
#     if name not in ['None', '']:
#         return {'short_name': name}
#     return {}
#
#
# def get_code(row):
#     try:
#         gpi = row['G_PlaceId']
#     except KeyError:
#         return {}
#     if gpi not in ['None', '']:
#         return {'code': gpi}
#     return {}
#
#
# def get_type(row):
#     try:
#         types = row['G_Types']
#     except KeyError:
#         return {}
#     if types not in ['None', '']:
#         return {'type': types}
#     return {}


def get_center(row):
    try:
        lat = row['G_Coordinates_location_Lat_3']
        lon = row['G_Coordinates_location_Lng_3']
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


def get_bounds(row):
    try:
        ne_lat = row['G_Coordinates_northeast_Lat_1']
        ne_lng = row['G_Coordinates_northeast_Lng_1']
        sw_lat = row['G_Coordinates_southwest_Lat_2']
        sw_lng = row['G_Coordinates_southwest_Lng_2']
    except KeyError:
        return {}
    if 'None' not in [ne_lat, sw_lat, ne_lng, sw_lng]:
        bounds = {'bounds':
                      {'left': {'lat':float(ne_lat), 'lng': float(ne_lng)},
                       'right': {'lat':float(sw_lat), 'lng': float(sw_lng)}}
                  }
        return bounds
    return {}
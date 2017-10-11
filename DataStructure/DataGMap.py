def parser_gmap(line):
    gmap_res = {}

    data_parser = (
        ('G_Locality_long_name', 'name'),
        ('G_Locality_short_name', 'short_name'),
        ('G_PlaceId', 'code'),
        ('G_Types', 'type'),
        ('G_FormatAddress', 'full_address'),
        ('G_postal_code_long_name', 'postal_code'),
    )

    for value in data_parser:
        gmap_res.update(pars(line, value[0], value[1]))

    functions_parser = (
        get_center,
        get_bounds,
        hierarchy,
        get_other,
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


def get_center(row):
    try:
        lat = row['G_Coordinates_location_Lat_3']
        lng = row['G_Coordinates_location_Lng_3']
    except KeyError:
        return {}
    if 'None' not in [lat, lng]:
        coordinates = {'center': {
                                  'lat': float(lat),
                                  'lng': float(lng),
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
        bounds = {'bounds': {
                            'left': {'lat': float(ne_lat), 'lng': float(ne_lng)},
                            'right': {'lat': float(sw_lat), 'lng': float(sw_lng)},
                            }
                  }
        return bounds
    return {}


def admin_level(row, identificator):
    dct_country = {}
    try:
        long_name = row['G_{}_long_name'.format(identificator)]
        short_name = row['G_{}_short_name'.format(identificator)]
        types = row['G_{}_types'.format(identificator)]
    except KeyError:
        return dct_country
    if 'None' not in [long_name, short_name, types]:
        dct_country.update({
            'name': long_name,
            'short_name': short_name,
            'type': types,
        })
    return dct_country


def hierarchy(row):
    admin_hierarchy = []
    for idn in ['Country', 'AdminLevel_1', 'AdminLevel_2']:
        val_level = admin_level(row, idn)
        if val_level:
            admin_hierarchy.append(val_level)
        else:
            return {}
    return {'admin_hierarchy': admin_hierarchy}


def get_other(row):
    other = {}
    other_gmap = [
        'G_Name_en',
        'G_Name_ru',
        'G_Name_uk',
    ]
    for name_column in other_gmap:
        try:
            value = row[name_column]
        except KeyError:
            continue
        if value not in ['', 'None']:
            other.update({name_column: value})
    if other:
        return other
    return {}

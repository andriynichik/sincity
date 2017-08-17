from lib.parser.Parser import Parser as Parser


class GMap(Parser):

    ADMIN_LEVEL_1 = 'country'
    ADMIN_LEVEL_2 = 'administrative_area_level_1'
    ADMIN_LEVEL_3 = 'administrative_area_level_2'
    ADMIN_LEVEL_4 = 'administrative_area_level_3'
    ADMIN_LEVEL_5 = 'administrative_area_level_4'
    ADMIN_LEVEL_6 = 'administrative_area_level_5'
    ADMIN_LEVEL_7 = 'locality'
    ADMIN_LEVEL_8 = 'sublocality_level_1'
    ADMIN_LEVEL_9 = 'sublocality_level_2'
    ADMIN_LEVEL_10 = 'sublocality_level_3'
    ADMIN_LEVEL_11 = 'sublocality_level_4'
    ADMIN_LEVEL_12 = 'sublocality_level_5'
    ADMIN_LEVEL_13 = 'sublocality'
    ADMIN_LEVEL_14 = 'neighborhood'

    POST_CODE = 'postal_code'

    QUANTITY_OF_ADMIN_LEVELS = 14

    def __init__(self, content):
        self._content = content
        self._admin_levels = []
        for x in range(1, self.QUANTITY_OF_ADMIN_LEVELS + 1):
            self._admin_levels.append(getattr(self, 'ADMIN_LEVEL_%d' % (x)))

    def as_dictionary(self):
        dic = {}

        place_id = self.get_place_id()
        if place_id:
            dic.update(code=place_id)

        long_name = self.get_long_name()
        if long_name:
            dic.update(name=long_name)

        short_name = self.get_short_name()
        if long_name:
            dic.update(short_name=short_name)

        type = self.get_type()
        if type:
            dic.update(type=type)

        admin_hierarchy = self.get_admin_hierarchy()
        if admin_hierarchy:
            dic.update(admin_hierarchy=admin_hierarchy)

        center_lat = self.get_center_latitude()
        center_lng = self.get_center_longitude()
        if center_lat and center_lng:
            dic.update(center={
                'lat': center_lat,
                'lng': center_lng
            })

        left_latitude = self.get_left_latitude()
        left_longitude = self.get_left_longitude()
        right_latitude = self.get_right_latitude()
        right_longitude = self.get_right_longitude()
        if left_latitude and left_longitude and right_latitude and right_longitude:
            dic.update(bounds={
                'left': {'lat': left_latitude, 'lng': left_longitude},
                'right': {'lat': right_latitude, 'lng': right_longitude},
            })

        postal_code = self.get_post_code()
        if postal_code:
            dic.update(postal_code=postal_code)

        return dic

    def get_center_latitude(self):
        #result = None
        #if 'geometry' in self._content and 'location' in self._content.get('geometry') and 'lat' in self._content.get('geometry').get('location'):
        #    result = self._content.get('geometry').get('location').get('lat')

        #return result
        return self._content.get('geometry', {}).get('location', {}).get('lat', None)

    def get_center_longitude(self):
        #result = None
        #if 'geometry' in self._content and 'location' in self._content.get('geometry') and 'lng' in self._content.get('geometry').get('location'):
        #    result = self._content.get('geometry').get('location').get('lng')

        #return result
        return self._content.get('geometry', {}).get('location', {}).get('lng', None)

    def get_left_latitude(self):
        #result = None
        #if 'geometry' in self._content and 'viewport' in self._content.get('geometry') and 'southwest' in self._content.get('geometry').get('viewport') and 'lat' in self._content.get('geometry').get('viewport').get('southwest'):
        #    result = self._content.get('geometry').get('viewport').get('southwest').get('lat')

        #return result
        return self._content.get('geometry', {}).get('viewport', {}).get('southwest', {}).get('lat', None)

    def get_left_longitude(self):
        #result = None
        #if 'geometry' in self._content and 'viewport' in self._content.get('geometry') and 'southwest' in self._content.get('geometry').get('viewport') and 'lng' in self._content.get('geometry').get('viewport').get('southwest'):
        #    result = self._content.get('geometry').get('viewport').get('southwest').get('lng')

        #return result
        return self._content.get('geometry', {}).get('viewport', {}).get('southwest', {}).get('lng', None)

    def get_right_latitude(self):
        #result = None
        #if 'geometry' in self._content and 'viewport' in self._content.get('geometry') and 'southwest' in self._content.get('geometry').get('viewport') and 'lat' in self._content.get('geometry').get('viewport').get('northeast'):
        #    result = self._content.get('geometry').get('viewport').get('northeast').get('lat')

        #return result
        return self._content.get('geometry', {}).get('viewport', {}).get('northeast', {}).get('lat', None)

    def get_right_longitude(self):
        #result = None
        #if 'geometry' in self._content and 'viewport' in self._content.get('geometry') and 'southwest' in self._content.get('geometry').get('viewport') and 'lng' in self._content.get('geometry').get('viewport').get('northeast'):
        #    result = self._content.get('geometry').get('viewport').get('northeast').get('lng')

        #return result
        return self._content.get('geometry', {}).get('viewport', {}).get('northeast', {}).get('lng', None)

    def get_place_id(self):
        return self._content.get('place_id', None)

    def get_long_name(self):
        return self._content.get('address_components')[0].get('long_name') if 'address_components' in self._content and len(self._content.get('address_components')) and 'long_name' in self._content.get('address_components')[0] else None

    def get_short_name(self):
        return self._content.get('address_components')[0].get('short_name') if 'address_components' in self._content and len(self._content.get('address_components')) and 'short_name' in self._content.get('address_components')[0] else None

    def get_type(self):
        result = None
        if 'address_components' in self._content and len(self._content.get('address_components')):
            element = self._parse_admin_element(self._content.get('address_components')[0])
            if 'type' in element:
                result = element.get('type')

        return result

    def get_admin_hierarchy(self):
        result = []
        if 'address_components' in self._content:
            admin_elements = reversed(self._content.get('address_components')[1:])
            for element in admin_elements:
                parsed_element = self._parse_admin_element(element)
                if 'type' in parsed_element and ('short_name' in parsed_element or 'long_name' in parsed_element):
                    result.append(parsed_element)

        return result

    def _parse_admin_element(self, element):
        result = {}
        if 'long_name' in element:
            result.update(name=element.get('long_name'))
        if 'short_name' in element:
            result.update(short_name=element.get('short_name'))

        if 'types' in element:
            type = self._get_admin_type(element.get('types'))
            if type:
                result.update(type=type)

        return result

    def _get_admin_type(self, target):
        result = None
        for level in self._admin_levels:
            if self._has_value_in_list(search=level, target_list=target):
                result = level
                break

        return result

    @staticmethod
    def _has_value_in_list(search, target_list):
        result = False
        try:
            result = target_list.index(search) is not None
        except:
            pass

        return result

    def get_post_code(self):
        result = None
        if 'address_components' in self._content:
            admin_elements = reversed(self._content.get('address_components'))
            for element in admin_elements:
                if 'types' in element and self._has_value_in_list(self.POST_CODE, element.get('types')):
                    short_name = element.get('short_name', '')
                    long_name = element.get('long_name', '')
                    result = short_name if short_name else long_name
                    break

        return result

    def get_address(self):
        return self._content.get('formatted_address', None)
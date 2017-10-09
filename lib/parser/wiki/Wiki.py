import re
from lib.parser.Parser import Parser as Parser


class Wiki(Parser):
    HOST = 'https://wikipedia.org'

    NAME = 'name'
    ADMIN_HIERARCHY = 'admin_hierarchy'
    LATITUDE = 'latitude'
    LONGITUDE = 'longitude'
    ALTITUDE = 'altitude'
    POPULATION = 'population'
    DENSITY = 'density'
    AREA = 'area'
    POSTAL_CODES = 'postal_codes'
    LANG_LINKS = 'lang_links'

    ADMIN_LEVEL_1 = ''
    ADMIN_LEVEL_2 = ''
    ADMIN_LEVEL_3 = ''
    ADMIN_LEVEL_4 = ''
    ADMIN_LEVEL_5 = ''
    ADMIN_LEVEL_6 = ''

    def __init__(self, content):
        super(Wiki, self).__init__(content=content)

    def get_main_block(self):
        pass

    def as_dictionary(self):
        dic = {}

        dic.update(name=self.get_name())

        type = self.get_type()
        if type:
            dic.update(type=type)

        admin = self.get_admin_hierarchy()
        if admin:
            dic.update(admin_hierarchy=self.get_admin_hierarchy())

        dic.update(i18n=self.get_lang_links())

        capital = self.get_capital()
        if capital:
            dic.update(capital=capital)

        lat = self.get_latitude()
        lng = self.get_longitude()
        if lat and lng:
            dic.update(center={
                'lat': lat,
                'lng': lng
            })

        altitude = self.get_altitude()
        if altitude:
            dic.update(altitude=altitude)

        population = self.get_population()
        if population:
            dic.update(population=population)

        density = self.get_density()
        if density:
            dic.update(density=density)

        area = self.get_area()
        if area:
            dic.update(area=area)

        postal_codes = self.get_postal_codes()
        if postal_codes:
            dic.update(postal_codes=postal_codes)

        residents = self.get_residents()
        if residents:
            dic.update(residents=residents)

        return dic

    def get_name(self):
        pass

    def get_type(self):
        pass

    def get_admin_hierarchy(self):
        '''
        contain short name, long name, type and tree for hierarchy or sort bya index
        '''
        pass

    def get_latitude(self):
        result = None

        block = self._content_soap.find("a", {"class": "mw-kartographer-maplink"})
        if block:
            result = float(block["data-lat"])

        if not result:
            block = self._content_soap.find("span", {"class": "geo"})
            match = re.search(r"(?P<lat>[\d\.]+);", str(block))
            if match:
                result = match.group('lat')

        #match = re.search(r"data-lat=\"(?P<lat>[\d\.]+)\"", self.content)
        #if match.group('lat'):
        #    result = match.group('lat')
        return result

    def get_longitude(self):
        result = None

        block = self._content_soap.find("a", {"class": "mw-kartographer-maplink"})
        if block:
            result = float(block["data-lon"])

        if not result:
            block = self._content_soap.find("span", {"class": "geo"})
            match = re.search(r";\s*(?P<lon>[\d\.]+)", str(block))
            if match:
                result = match.group('lon')

        #match = re.search(r"data-lon=\"(?P<lon>[\d\.]+)\"", self.content)
        #if match.group('lon'):
        #    result = match.group('lon')
        return result

    def get_altitude(self):
        pass

    def _get_min_altitude(self, content):
        result = None
        match = re.search(r"(?i)Min\.?\s*(?P<min>\d+)", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        if match:
            result = float(match.group('min').replace(',', '.'))
        return result

    def _get_max_altitude(self, content):
        result = None
        match = re.search(r"(?i)Max\.?\s*(?P<max>\d+)", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        if match:
            result = float(match.group('max').replace(',','.'))
        return result

    def get_population(self):
        pass

    def get_density(self):
        pass

    def get_area(self):
        pass

    def get_postal_codes(self):
        pass

    def get_residents(self):
        pass

    def get_capital(self):
        pass

    def get_lang_links(self):
        result = {}

        tags = self._content_soap.find_all('li', {"class": "interlanguage-link"})
        for tag in tags:
            match = re.search(r"(?P<name>.*?) [-—] ", tag.a['title'])
            if match:
                name = match.group('name')
                result[tag.a["lang"]] = {"name": name, "url": tag.a["href"]}

        #match = re.search(r"(?i)<li[^>]+class\s*=\s*[\"'][^\"']*interlanguage[^\"]*[\"'].*?href=[\"'](?P<url>.*?)[\"'][^>]*?title=[\"']\s*(?P<name>.*?)\s*—[^\"']*[\"'].*?lang=[\"'](?P<lang>\w+)[\"']",
        #                  self.content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        #if match.group('url'):
        #    urls = match.group('url')
        #    langs = match.group('lang')
        #    names = match.group('name')
        #    for key, lang in langs:
        #        result[lang] = {'name': names[key], 'url':urls[key]}

        return result

    def is_location_page(self):
        pass

    def is_many_answers(self):
        return bool(self._content_soap.find("div", {"class": "results-info"}))
        #match = re.search(r"(class=\"results-info\")", self.content)
        #return bool(match.group(0))

    def get_answers_links(self):
        tags = self._content_soap.find_all("div", {"class": "mw-search-result-heading"})
        return [(self.HOST + x.a["href"]) for x in tags if re.match(r"(/wiki/)", x.a["href"])]

        #match = re.search(r"<div[^>]*?class=[\"']mw-search-result-heading[\"'][^>]*?>\s*<a href=[\"'](?P<url>/wiki/[^\"]+)[\"']", self.content)
        #return [(self.HOST + x) for x in match.group('url')]

    def _is_range(self, content):
        return re.match(r"\d+-\d+", content) is not None

    def _range(self, content):
        codes = []
        match = re.search(r"(?P<start>\d+)-(?P<end>\d+)", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        if match:
            start = int(match.group('start'))
            end = int(match.group('end'))
            if start > end:
                start, end = end, start
            codes = range(start, end + 1, 1)
        return codes

    def _parse_postal_code(self, codes):
        find_codes = []
        if self._is_range(codes):
            find_codes += self._range(codes)
        else:
            find_codes.append(int(codes))
        return find_codes

    def _first_numbers(self, content):
        match = re.search(r"^(?P<number>([\d,\.]+))", content.replace(' ', ''))
        return match.group('number').strip(',.').replace(',', '.') if match else 0

    def _get_value_with_link(self, column_name, content):
        match = re.search(
            r"<th[^>]*>(.(?!<th))*" + re.escape(column_name) + r"(.(?!<th))*<[^>]*th>\s*<td[^>]*>.*?<a[^>]*href=\"(?P<url>/wiki/[^\"]*)\"[^>]*>(?P<name>[^<]*)</a>.*?<[^>]*td>",
            content,
            re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)

        return {"url": self.HOST + match.group('url'), "name": self.replace_html(match.group('name'))} if match else {}

    def _get_value(self, column_name, content):
        match = re.search(
            r"<th[^>]*>.*?" + re.escape(column_name) + r".*?<[^>]*th>\s*<td[^>]*>(?P<name>.*?)<[^>]*td>",
            content,
            re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)

        return self.replace_html(match.group('name')) if match else None

    def get_all_links(self):
        links = super(Wiki, self).get_all_links()
        return [(self.HOST + x) for x in links if re.match(r"(/wiki/)", x)]
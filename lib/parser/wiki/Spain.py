import re
from lib.parser.wiki.Wiki import Wiki as Wiki


class Spain(Wiki):

    HOST = 'https://es.wikipedia.org'
    ADMIN_LEVEL_1 = u'país'
    ADMIN_LEVEL_2 = u'autónoma'
    ADMIN_LEVEL_3 = u'provincia'
    ADMIN_LEVEL_4 = u'comarca'
    ADMIN_LEVEL_5 = u'partido_judicial'
    ADMIN_LEVEL_6 = u'Municipio'

    def __init__(self, content):
        super(Spain, self).__init__(content)
        self._main_block = str(self.get_main_block())

    def get_main_block(self):
        content = self._content_soap.find("table", { "class" : "infobox geography vcard" })
        return content

    def as_dictionary(self):
        dic = super(Spain, self).as_dictionary()

        frazioni = self.get_frazioni()
        if frazioni:
            dic.update(frazioni=frazioni)

        istat = self.get_istat()
        if istat:
            dic.update(istat=istat)

        catastale = self.get_catastale()
        if catastale:
            dic.update(catastale=catastale)

        return dic

    def get_name(self):
        name_raw = self._content_soap.select_one('#firstHeading')
        if not name_raw:
            name_raw = self._content_soap.select_one('table.sinottico > tbody > tr.sinottico_testata > th')

        return self.replace_html(str(name_raw)) if name_raw else ''

    def get_type(self):
        element = str(self._content_soap.select_one('table.sinottico > tr.sinottico_testata'))
        if element:
            match = re.search(r"(?P<type>{})".format(self.ADMIN_LEVEL_6), element,
                              re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
            if match:
                return self.ADMIN_LEVEL_6

            match = re.search(r"(?P<type>{})".format(self.ADMIN_LEVEL_5), element, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
            if match:
                return self.ADMIN_LEVEL_5

            match = re.search(r"(?P<type>{})".format(self.ADMIN_LEVEL_4), element, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
            if match:
                return self.ADMIN_LEVEL_4

            match = re.search(r"(?P<type>{})".format(self.ADMIN_LEVEL_3), element, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
            if match:
                return self.ADMIN_LEVEL_3

            match = re.search(r"(?P<type>{})".format(self.ADMIN_LEVEL_2), element, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
            if match:
                return self.ADMIN_LEVEL_2

            match = re.search(r"(?P<type>{})".format(self.ADMIN_LEVEL_1), element, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
            if match:
                return self.ADMIN_LEVEL_1

        return None

    def get_admin_hierarchy(self):
        admin = {}

        min_level = self.get_type()

        if min_level == self.ADMIN_LEVEL_1:
            return admin

        country = self._get_country()
        if country and country.get('name', None):
            admin.update(ADMIN_LEVEL_1=country)

        if min_level == self.ADMIN_LEVEL_2:
            return admin

        region = self._get_region()
        if region and region.get('name', None):
            admin.update(ADMIN_LEVEL_2=region)

        if min_level == self.ADMIN_LEVEL_3:
            return admin

        department = self._get_department()
        if department and department.get('name', None):
            admin.update(ADMIN_LEVEL_3=department)

        if min_level == self.ADMIN_LEVEL_4:
            return admin

        borough = self._get_borough()
        if borough and borough.get('name', None):
            admin.update(ADMIN_LEVEL_4=borough)

        if min_level == self.ADMIN_LEVEL_5:
            return admin

        city = self._get_city()
        if city and city.get('name', None):
            admin.update(ADMIN_LEVEL_5=city)

        return admin

    def _get_country(self):
        result = self._get_value_with_link(u"País", self._main_block)
        result.update(type=self.ADMIN_LEVEL_1)
        return result

    def _get_region(self):
        result = self._get_value_with_link(u"Com. autónoma", self._main_block)
        result.update(type=self.ADMIN_LEVEL_2)
        return result

    def _get_department(self):
        result = self._get_value_with_link(u"Provincia", self._main_block)
        if result:
            result.update(type=self.ADMIN_LEVEL_3)
        return result

    def _get_borough(self):
        result = self._get_value_with_link(u"Comarca", self._main_block)
        if result:
            result.update(type=self.ADMIN_LEVEL_4)
        return result

    def _get_city(self):
        result = self._get_value_with_link(u"Partido judicial", self._main_block)
        if result:
            result.update(type=self.ADMIN_LEVEL_5)
        return result

    def get_altitude(self):
        result = None
        data = str(self._get_value(u'Altitud', self._main_block))

        if data:
            result = self._first_numbers(str(data))

        return result

    def get_population(self):
        population = self._get_value(u"Población", self._main_block)
        first_numbers = self._first_numbers(str(population))
        first_numbers = re.sub(r"\.", "", str(first_numbers), re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)

        return int(first_numbers) if first_numbers else 0

    def get_density(self):
        data = self._get_value(u"Densidad", self._main_block)
        first_numbers = self._first_numbers(str(data))

        return float(first_numbers) if first_numbers else 0

    def get_area(self):
        data = self._get_value(u'Superficie', self._main_block)
        first_numbers = float(self._first_numbers(str(data)))

        return first_numbers if first_numbers else None

    def get_capital(self):
        result = None
        capital = self._get_value_with_link(u"Capoluogo", self._main_block)
        if capital:
            result = capital

        return result

    def get_postal_codes(self):
        data = self._get_value('Código postal', self._main_block)
        return self._parse_postal_codes(data) if data else ''

    def _parse_postal_codes(self, content):
        codes = []
        content = re.sub(r"(?i)(\s+|^)a(\s+|$)", "-", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        content = re.sub(r"(?i)(\s+|^)e(\s+|$)", ",", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        content = re.sub(r";", ",", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        content = re.sub(r"–", "-", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        content = re.sub(r"(?i)\s*da\s*", ",", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        content = re.sub(r"(\D|^)\s*-\s*(\D|$)", " ", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        content = re.sub(r"[^\d,-]+", " ", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        content = re.sub(r"\s+", ",", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)

        for code_bloc in content.split(','):
            if code_bloc:
                codes += self._parse_postal_code(code_bloc)

        good_codes = []

        for code in codes:
            code = str(code)
            code_len = len(code)
            if code_len < 5:
                zeros = ['0'] * (5 - code_len)
                zeros.append(code)
                good_codes.append(''.join(zeros))
            else:
                good_codes.append(code)

        return good_codes

    def is_location_page(self):
        match = re.search(r"href=[\"']/wiki/Template:Divisione_amministrativa/man[\"']",
            self._main_block, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        return bool(match)


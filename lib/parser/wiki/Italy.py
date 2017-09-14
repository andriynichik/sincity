import re
from lib.parser.wiki.Wiki import Wiki as Wiki


class Italy(Wiki):

    HOST = 'https://it.wikipedia.org'
    ADMIN_LEVEL_1 = u'stato'
    ADMIN_LEVEL_2 = u'regione'
    ADMIN_LEVEL_3 = u'provincia'
    ADMIN_LEVEL_4 = u'città metropolitana'
    ADMIN_LEVEL_5 = u'comune'

    def __init__(self, content):
        super(Italy, self).__init__(content)
        self._main_block = str(self.get_main_block())

    def get_main_block(self):
        content = self._content_soap.find("table", { "class" : "sinottico" })
        return content

    def as_dictionary(self):
        dic = super(Italy, self).as_dictionary()
        return dic

    def get_name(self):
        name_raw = self._content_soap.select_one('#firstHeading')
        if not name_raw:
            name_raw = self._content_soap.select_one('table.sinottico > tbody > tr.sinottico_testata > th')

        return self.replace_html(str(name_raw)) if name_raw else ''

    def get_type(self):
        element = str(self._content_soap.select_one('table.sinottico > tr.sinottico_testata'))
        if element:
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
        admin = []

        country = self._get_country()
        if country:
            admin.append(country)

        region = self._get_region()
        if region:
            admin.append(region)

        department = self._get_department()
        if department:
            admin.append(department)

        borough = self._get_borough()
        if borough:
            admin.append(borough)

        city = self._get_city()
        if city:
            admin.append(city)

        return admin

    def _get_country(self):
        result = self._get_value_with_link(u"Stato", self._main_block)
        result.update(type=self.ADMIN_LEVEL_1)
        return result

    def _get_region(self):
        result = self._get_value_with_link(u"Regione", self._main_block)
        result.update(type=self.ADMIN_LEVEL_2)
        return result

    def _get_department(self):
        result = self._get_value_with_link(u"Provincia", self._main_block)
        if result:
            result.update(type=self.ADMIN_LEVEL_3)
        return result

    def _get_borough(self):
        result = self._get_value_with_link(u"Città metropolitana", self._main_block)
        if result:
            result.update(type=self.ADMIN_LEVEL_4)
        return result

    def _get_city(self):
        result = self._get_value_with_link(u"Comune", self._main_block)
        if result:
            result.update(type=self.ADMIN_LEVEL_5)
        return result

    def get_altitude(self):
        result = None
        data = str(self._get_value(u'Altitudine', self._main_block))

        if data:
            result = self._first_numbers(data)

        return result

    def get_population(self):
        population = self._get_value(u"Abitanti", self._main_block)
        first_numbers = self._first_numbers(str(population))

        return int(first_numbers) if first_numbers else 0

    def get_density(self):
        data = self._get_value(u"Densità", self._main_block)
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
        data = self._get_value('Cod. postale', self._main_block)
        return self._parse_postal_codes(data) if data else ''

    def _parse_postal_codes(self, content):
        codes = []
        content = re.sub(r"(?i)\s*a\s*", "-", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        content = re.sub(r"–", "-", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        content = re.sub(r"(?i)\s*da\s*", ",", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        content = re.sub(r"\s+", "", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        for code_bloc in content.split(','):
            codes += self._parse_postal_code(code_bloc)

        return codes

    def _parse_commune_codes(self, content):
        return self._parse_postal_codes(content)
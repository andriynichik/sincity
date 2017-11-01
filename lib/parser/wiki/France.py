import re
from lib.parser.wiki.Wiki import Wiki as Wiki


class France(Wiki):

    HOST = 'https://fr.wikipedia.org'
    ADMIN_LEVEL_1 = u'pays'
    ADMIN_LEVEL_2 = u'région'
    ADMIN_LEVEL_3 = u'département'
    ADMIN_LEVEL_4 = u'arrondissement'
    ADMIN_LEVEL_5 = u'canton'
    ADMIN_LEVEL_6 = u'intercommunalité'
    ADMIN_LEVEL_7 = u'commune'

    def __init__(self, content):
        super(France, self).__init__(content)
        self._main_block = str(self.get_main_block())


    def as_dictionary(self):
        dic = super(France, self).as_dictionary()

        communes = self.get_communes()
        if communes:
            dic.update(communes=communes)

        canton_codes = self.get_canton_codes()
        if canton_codes:
            dic.update(canton_codes=canton_codes)

        insee = self.get_code_insee()
        if insee:
            dic.update(insee=insee)

        commune_codes = self.get_commune_codes()
        if commune_codes:
            dic.update(commune_codes=commune_codes)

        return dic

    def get_main_block(self):
        content = self._content_soap.find("table", { "class" : "infobox_v2" })
        if not content:
            content = self._content_soap.find("table", { "class" : "infobox_v3" })
        return content

    def get_name(self):
        name_raw = self._content_soap.select_one('#firstHeading')
        if not name_raw:
            name_raw = self._content_soap.select_one('tr:nth-child(1) > td')

        return self.replace_html(str(name_raw)) if name_raw else ''

    def get_type(self):
        text = None
        match = re.search(
            r'href=["\']/wiki/Mod%C3%A8le:Infobox_(?P<code>Pays|(R%C3%A9gion|D%C3%A9partement|Arrondissement|Canton|Intercommunalit%C3%A9|Commune)_de_France)["\']',
            self._main_block, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        if match:
            text = match.group('code')
            text = self._url_decode(text).replace('_de_France', '').lower()
        return text

    def get_admin_hierarchy(self):
        admin = {}

        min_level = self.get_type()

        if min_level == self.ADMIN_LEVEL_1:
            return admin

        country = self._get_level_1()
        if country:
            admin.update(ADMIN_LEVEL_1=country)

        if min_level == self.ADMIN_LEVEL_2:
            return admin

        region = self._get_level_2()
        if region:
            admin.update(ADMIN_LEVEL_2=region)

        if min_level == self.ADMIN_LEVEL_3:
            return admin

        department = self._get_level_3()
        if department:
            admin.update(ADMIN_LEVEL_3=department)

        if min_level == self.ADMIN_LEVEL_4:
            return admin

        borough = self._get_level_4()
        if borough:
            admin.update(ADMIN_LEVEL_4=borough)

        if min_level == self.ADMIN_LEVEL_5:
            return admin

        canton = self._get_level_5()
        if canton:
            admin.update(ADMIN_LEVEL_5=canton)

        if min_level == self.ADMIN_LEVEL_6:
            return admin


        metropole = self._get_level_6()
        if metropole:
            admin.update(ADMIN_LEVEL_6=metropole)

        return admin

    def _get_level_1(self):
        result = self._get_value_with_link(u"Pays", self._main_block)
        result.update(type=self.ADMIN_LEVEL_1)
        return result

    def _get_level_2(self):
        result = self._get_value_with_link(u"Région", self._main_block)
        result.update(type=self.ADMIN_LEVEL_2)
        return result

    def _get_level_3(self):
        result = self._get_value_with_link(u"Département", self._main_block)
        if result:
            result.update(type=self.ADMIN_LEVEL_3)
        return result

    def _get_level_4(self):
        result = self._get_value_with_link(u"Arrondissement", self._main_block)
        if result:
            result.update(type=self.ADMIN_LEVEL_4)
        return result

    def _get_level_5(self):
        result = self._get_value_with_link(u"Canton", self._main_block)
        if result:
            result.update(type=self.ADMIN_LEVEL_5)
        return result

    def _get_level_6(self):
        result = self._get_value_with_link(u"Intercommunalité", self._main_block)
        if result:
            result.update(type=self.ADMIN_LEVEL_6)
        return result

    def get_altitude(self):
        result = {}
        data = str(self._get_value(u'Altitude', self._main_block))

        min = self._get_min_altitude(data)
        if min is not None:
            result.update(min=min)

        max = self._get_max_altitude(data)
        if max is not None:
            result.update(max=max)

        return result

    def get_population(self):
        population = self._get_value(u"Population", self._main_block)
        first_numbers = self._first_numbers(str(population))

        return int(first_numbers) if first_numbers else 0

    def get_density(self):
        data = self._get_value(u"Densité", self._main_block)
        first_numbers = self._first_numbers(str(data))

        return float(first_numbers) if first_numbers else 0

    def get_area(self):
        data = self._get_value(u'Superficie', self._main_block)
        first_numbers = float(self._first_numbers(str(data)))

        return first_numbers if first_numbers else None

    def get_capital(self):

        capital = self._get_value_with_link(u"Siège", self._main_block)
        if capital:
            return capital

        capital = self._get_value_with_link(u"Siège de la préfecture", self._main_block)
        if capital:
            return capital

        capital = self._get_value_with_link(u"Chef-lieu", self._main_block)
        if capital:
            return capital

        capital = self._get_value_with_link(u"Capitale", self._main_block)
        if capital:
            return capital

        return None

    def get_communes(self):
        return self._get_value(u'Communes', self._main_block)

    def get_canton_codes(self):
        return self._get_value(u'Code canton', self._main_block)

    def get_code_insee(self):
        return self._get_value(u'Code Insee', self._main_block)

    def get_postal_codes(self):
        data = self._get_value('Code postal', self._main_block)
        return self._parse_postal_codes(data) if data else ''

    def get_commune_codes(self):
        data = self._get_value('Code commune', self._main_block)
        return self._parse_commune_codes(data) if data else ''

    def is_location_page(self):
        match = re.search(r"href=[\"']/wiki/Mod%C3%A8le:Infobox_(?P<code>Pays|(R%C3%A9gion|D%C3%A9partement|Arrondissement|Canton|Intercommunalit%C3%A9|Commune)_de_France)[\"']",
            self._main_block, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        return bool(match)

    def _parse_postal_codes(self, content):
        codes = []
        content = re.sub(r"(?i)\s*à\s*", "-", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        content = re.sub(r"(?i)\s*et(\s+de)?\s*", ",", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        content = re.sub(r"\s+", "", content, re.MULTILINE | re.UNICODE | re.IGNORECASE | re.DOTALL)
        for code_bloc in content.split(','):
            codes += self._parse_postal_code(code_bloc)

        return codes

    def _parse_commune_codes(self, content):
        return self._parse_postal_codes(content)

    def get_residents(self):
        result = self._get_value(u"Gentilé", self._main_block)
        return result if result else ''

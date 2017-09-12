from lib.location.Location import Location


class Internal(Location):

    TYPE = 'internal'

    def _add_source(self, name, value):
        data = self._get_obj()
        if not data[name]:
            data[name] = []
        if value not in data[name]:
            data[name].append(value)

        self._storage.save({'code': self.code}, data)

    def _remove_source(self, name, value):
        data = self._get_obj()
        if data[name]:
            data[name] = [x for x in data[name] if x != value]


    def add_wiki_source(self, code):
        self._add_source('wiki', code)

    def add_google_map_source(self, code):
        self._add_source('gmaps', code)

    def get_wiki_sources(self):
        data = self._get_obj()
        return data.wiki if data.wiki else []

    def get_google_map_sources(self):
        data = self._get_obj()
        return data.gmaps if data.gmaps else []
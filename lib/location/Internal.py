from lib.location.Location import Location


class Internal(Location):

    TYPE = 'internal'

    def __init__(self, code, storage):
        collection = storage[self.TYPE]
        super(Internal, self).__init__(code=code, storage=collection)

    def _add_source(self, name, value):
        data = self.get_document()
        if not data.get(name):
            data.update({name: ''})
        else:
            data.update({name: value})

        self.update(data)

    def _remove_source(self, name, value):
        data = self.get_document()
        if data.get(name):
            data.update({name: ''})
            self.update(data)

    def add_wiki_source(self, code):
        self._add_source('wiki', code)

    def add_google_map_source(self, code):
        self._add_source('gmaps', code)

    def get_wiki_sources(self):
        data = self.get_document()
        return data.get('source',{}).get('wiki')

    def get_google_map_sources(self):
        data = self.get_document()
        return data.get('source',{}).get('gmap')

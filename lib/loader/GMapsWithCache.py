from lib.loader.GMaps import GMaps
import json


class LoaderGMapsWithCache(GMaps):
    def __init__(self, googlemaps, storage, language=None):
        super(LoaderGMapsWithCache, self).__init__(googlemaps=googlemaps, language=language)
        self._storage = storage

    def address_key(self, address):
        return ['address', address]

    def by_address(self, address, use_cache=True):
        result = {}
        key = self.address_key(address)
        if use_cache:
            result = self.from_cache(key)

        if not result:
            result = super(LoaderGMapsWithCache, self).by_address(address=address)
            self.to_cache(content=result, params=key)

        return result

    def position_key(self, lat, lng):
        return ['position', lat, lng]

    def by_position(self, lat, lng, use_cache=True):
        result = {}
        key = self.position_key(lat=lat, lng=lng)
        if use_cache:
            result = self.from_cache(key)

        if not result:
            result = super(LoaderGMapsWithCache, self).by_position(lat=lat, lng=lng)
            self.to_cache(content=result, params=key)

        return result

    def from_cache(self, params):
        result = None
        cache_data = self._storage.get(params)
        if cache_data:
            result = json.loads(cache_data)

        return result

    def to_cache(self, content, params):
        if content:
            self._storage.set(content=bytes(json.dumps(content), 'utf8'), params=params)
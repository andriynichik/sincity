class GMaps:
    def __init__(self, googlemaps, language=None):
        self._googlemaps = googlemaps
        self._language = language

    def by_address(self, address):
        return self._googlemaps.geocode(address, language=self._language)

    def by_position(self, lat, lng):
        return self._googlemaps.reverse_geocode((lat, lng), language=self._language)
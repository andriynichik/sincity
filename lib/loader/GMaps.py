class GMaps:
    def __init__(self, googlemaps, language=None):
        self._googlemaps = googlemaps
        self._language = language

    def by_address_and_components(self, address, components):
        return self._googlemaps.geocode(address, components=components, language=self._language)

    def by_place_id(self, place_id):
        return self._googlemaps.geocode(place_id=place_id, language=self._language)

    def by_component(self, components):
        return self._googlemaps.geocode(components=components, language=self._language)

    def by_address(self, address):
        return self._googlemaps.geocode(address, language=self._language)

    def by_position(self, lat, lng):
        return self._googlemaps.reverse_geocode((lat, lng), language=self._language)
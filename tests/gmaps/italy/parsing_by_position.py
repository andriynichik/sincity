from lib.factory.Loader import Loader as LoaderFactory
from lib.parser.map.google.GMapFactory import GMapFactory as MapFactory
from lib.config.Yaml import Yaml as Config


config = Config('./config/config.yml')

loader = LoaderFactory.loader_gmaps_with_cache(config.get('googlemaps'), config.get('mongodb'))

position_content = loader.by_position(lat=41.900, lng=12.500)

print(position_content)

print('.' if len(position_content) else 'E', end='')

objects = MapFactory.italy(position_content)

print('.' if len(objects) else 'E', end='')

from lib.factory.Loader import Loader as Factory
from lib.config.Yaml import Yaml as Config


config = Config('./config/config.yml')

print(config.get('googlemaps').get('geocoding').get('key'))

gmaps_config = config.get('googlemaps')
gmaps_config.update(language=None)

loader = Factory.loader_gmaps(gmaps_config)

lat, lng = 48.861077, 2.344552

position_content = loader.by_position(lat=lat, lng=lng)

print(position_content)

print('.' if len(position_content) else 'E', end='')

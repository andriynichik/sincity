from lib.factory.Loader import Loader as Factory
from lib.config.Yaml import Yaml as Config


config = Config('./config/config.yml')

gmaps_config = config.get('googlemaps')
gmaps_config.update(language=None)

loader = Factory.loader_gmaps(gmaps_config)

address = 'France, Paris'

address_content = loader.by_address(address=address)

print('.' if len(address_content) else 'E', end='')
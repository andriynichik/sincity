from lib.factory.Loader import Loader as Factory
from lib.config.Yaml import Yaml as Config


config = Config('./config/config.yml')

gmaps_config = config.get('googlemaps')
gmaps_config.update(language='it')

loader = Factory.loader_gmaps(gmaps_config)

address = 'Italie, Roma'

address_content = loader.by_address(address=address)

print(address_content)

print('.' if len(address_content) else 'E', end='')
from lib.factory.Loader import Loader as LoaderFactory
from lib.parser.map.google.GMapFactory import GMapFactory as MapFactory
from lib.config.Yaml import Yaml as Config


config = Config('./config/config.yml')

gmap_config = config.get('googlemaps')
gmap_config.update(language='fr')

loader = LoaderFactory.loader_gmaps_with_cache(gmaps_config=gmap_config, storage_config=config.get('mongodb'))

components = {'country': 'FR', 'postal_code': '25320'}

components_content = loader.by_component(components=components)

print(components_content)

print('.' if len(components_content) else 'E', end='')

objects = MapFactory.france(components_content)

print('.' if len(objects) else 'E', end='')

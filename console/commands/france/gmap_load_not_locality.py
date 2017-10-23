from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.factory.Loader import Loader
from lib.parser.map.google.France import France as gmapFrance
from lib.config.Yaml import Yaml as Config

config = Config('./config/config.yml')

doc_factory = DocFactory(config.get('mongodb'))

internal_docs = doc_factory.internal_collection()
gmap_docs = doc_factory.gmaps_collection()

gmap_config = config.get('googlemaps')
gmap_config.update(language='fr')

gmap_loader = Loader.loader_gmaps_with_cache(gmaps_config=gmap_config, storage_config=config.get('mongodb'))

document_filter = {
    'name': {'$exists': True, '$not': {'$size': 0}},
    '$and': [{'ADMIN_LEVEL_1': 'France'}]
}

objects = internal_docs.find(document_filter)

for obj in objects:
    pass
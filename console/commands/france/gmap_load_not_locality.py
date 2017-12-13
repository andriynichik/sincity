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
    '$and': [{'admin_hierarchy.ADMIN_LEVEL_1.name': 'France'}]
}

objects = internal_docs.find(document_filter)

print(objects.count())

#exlude_type = [
#    'administrative_area_level_1',
#    'administrative_area_level_2',
#    'locality,political',
#    'locality',

#    'political,sublocality,sublocality_level_1' # не понятно оставлять его или нет
#]

#replace = [
#    'establishment,point_of_interest,premise',
#    'postal_code',
#    'street_address',
#    'route'
#]

count = 0

for obj in objects:
    if obj.get('source', {}).get('gmap'):
        gmap_code = obj.get('source', {}).get('gmap')
        gmap_doc = gmap_docs.find_one({'code': gmap_code})
        type_doc = gmap_doc.get('type')

        if not gmap_doc.get('name'):
            count = count + 1
 #       if type_doc not in exlude_type and type_doc not in replace:
 #           print(type_doc)
 #           print(gmap_doc.get('name'))
 #           print(obj.get('name'))

print(count)
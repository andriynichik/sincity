from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.factory.Loader import Loader
from lib.config.Yaml import Yaml as Config
from lib.parser.map.google.GMapFactory import GMapFactory as MapFactory


config = Config('./config/config.yml')

doc_factory = DocFactory(config.get('mongodb'))

internal_docs = doc_factory.internal_collection()
gmap_docs = doc_factory.gmaps_collection()
wiki_docs = doc_factory.wiki_collection()

language = 'fr'

gmap_config = config.get('googlemaps')
gmap_config.update(language=language)

gmap_loader = Loader.loader_gmaps_with_cache(gmaps_config=gmap_config, storage_config=config.get('mongodb'))

document_filter = {
    'name': {'$exists': True, '$not': {'$size': 0}},
    '$and': [{'admin_hierarchy.ADMIN_LEVEL_1.name': 'France'}]
}

objects = internal_docs.find(document_filter)

print('total:' + str(objects.count()))

exlude_type = [
    'administrative_area_level_1',
    'administrative_area_level_2',
    'locality,political',
    'locality',
    'administrative_area_level_2,political',
    'administrative_area_level_2,political',
    'administrative_area_level_3',
    'political,sublocality,sublocality_level_1',
    'sublocality_level_1',
    'country'
]

replace = [
    'establishment,point_of_interest,premise',
    'postal_code',
    'street_address',
    'route',
    'establishment,health,insurance_agency,point_of_interest',
    'establishment,food,meal_takeaway,point_of_interest,restaurant,store',
    'establishment,point_of_interest',
    'car_repair,establishment,point_of_interest,store',
    'establishment,point_of_interest',
    'establishment,point_of_interest,shoe_store,store',
    'clothing_store,department_store,establishment,point_of_interest,store',
    'city_hall,establishment,local_government_office,point_of_interest',
    'bar,establishment,food,point_of_interest,restaurant',
    'establishment,point_of_interest,travel_agency',
    'establishment,point_of_interest',
    'campground,establishment,food,lodging,park,point_of_interest,real_estate_agency,restaurant,rv_park,travel_agency',
    'establishment,lodging,point_of_interest',
    'establishment,local_government_office,point_of_interest',
    'establishment,parking,point_of_interest',
    'establishment,point_of_interest,school',
    'clothing_store,establishment,point_of_interest,store',
    'establishment,lodging,point_of_interest',
    'establishment,park,point_of_interest',
    'city_hall,establishment,fire_station,local_government_office,point_of_interest',
    'establishment,natural_feature',
    'neighborhood,political',
    'colloquial_area,political',
    'establishment,funeral_home,point_of_interest',
    'establishment,hospital,point_of_interest',
    'atm,bank,establishment,finance,point_of_interest',
    'doctor,establishment,health,point_of_interest',
    'premise',
    'establishment,health,point_of_interest',
    'subpremise',
    'establishment,movie_theater,point_of_interest',
    'bar,establishment,food,lodging,night_club,point_of_interest,restaurant,spa',
    'car_repair,establishment,point_of_interest',
    'bank,establishment,finance,point_of_interest',
    'establishment,library,point_of_interest',
    'clothing_store,establishment,lodging,point_of_interest,store,travel_agency',
    'establishment,food,point_of_interest,restaurant',
    'establishment,lodging,point_of_interest,real_estate_agency,travel_agency',
    'establishment,point_of_interest,train_station,transit_station',
    'bar,establishment,food,meal_takeaway,point_of_interest,restaurant',
    'church,establishment,place_of_worship,point_of_interest',
    'car_rental,establishment,point_of_interest',
    'accounting,establishment,finance,point_of_interest',
    'establishment,natural_feature,point_of_interest',
    'establishment,food,lodging,point_of_interest,restaurant',
    'establishment,food,grocery_or_supermarket,point_of_interest,store',
    'establishment,home_goods_store,point_of_interest,store',
    'establishment,point_of_interest,zoo',
    'establishment,food,grocery_or_supermarket,point_of_interest,store',
    'bank,establishment,finance,insurance_agency,point_of_interest',
    'intersection',
    'campground,establishment,lodging,park,point_of_interest',
    'establishment,insurance_agency,point_of_interest',
    'establishment,jewelry_store,point_of_interest,store',
    'amusement_park,establishment,point_of_interest',
    'bank,establishment,finance,point_of_interest,post_office',
    'establishment,florist,point_of_interest,store',
    'establishment,lodging,point_of_interest,spa',
    'establishment,food,point_of_interest,restaurant,travel_agency',
    'campground,establishment,lodging,park,point_of_interest,rv_park,spa',
    'establishment,furniture_store,home_goods_store,point_of_interest,store',
    'establishment,point_of_interest,real_estate_agency,travel_agency',
    'campground,establishment,food,lodging,park,point_of_interest,restaurant',
    'car_dealer,establishment,point_of_interest,store'
]

def gmap_by_address(wiki):

    address = []
    for name, value in wiki.get('admin_hierarchy', {}).items():
        address.append(value.get('name'))
    address = address[0:3]
    address.append(wiki.get('name'))
    address_str = ','.join(address).replace('Agglomération', ' ').replace(' d\'', ' ').replace('Arrondissement de ', '').replace('Arrondissement ', '').replace('Canton de ', '')
    print(address_str)
    response = gmap_loader.by_address(address=address_str)
    map_objects = MapFactory.france(response)

    gmap_dic = {}
    if map_objects:
        gmap_dic = map_objects[0].as_dictionary()
        gmap_dic.update(language=language)

    return gmap_dic


empty_doc = 0
locality = 0
need_replace = 0

for obj in objects:
    if obj.get('source', {}).get('gmap'):
        gmap_code = obj.get('source', {}).get('gmap')
        wiki_code = obj.get('source', {}).get('wiki')
        gmap_doc = gmap_docs.find_one({'code': gmap_code})
        wiki_doc = wiki_docs.find_one({'code': wiki_code})
        type_doc = gmap_doc.get('type')

        if not type_doc:
            empty_doc = empty_doc + 1
            print(wiki_doc.get('type'))
            result = gmap_by_address(wiki_doc)
            if result:
                gmap_obj = doc_factory.gmaps(code=result.get('code'))
                doc = gmap_obj.get_document()
                gmap_obj.update(new_data=gmap_obj.get_document())

                source = obj.get('source', {})
                source.update(gmap=doc.get('code'))
                internal_docs.update_one({'code': obj.get('code')}, {'$set': {'source': source}})

        if type_doc in exlude_type:
            locality = locality + 1

        if type_doc in replace:
            need_replace = need_replace + 1
            print(wiki_doc.get('type'))
            result = gmap_by_address(wiki_doc)
            if result:
                gmap_obj = doc_factory.gmaps(code=result.get('code'))
                doc = gmap_obj.get_document()
                gmap_obj.update(new_data=gmap_obj.get_document())

                source = obj.get('source', {})
                source.update(gmap=doc.get('code'))
                internal_docs.update_one({'code': obj.get('code')}, {'$set': {'source': source}})

print('empty:' + str(empty_doc))
print('locality:' + str(locality))
print('need_replace:' + str(need_replace))
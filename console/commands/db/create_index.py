from pymongo import MongoClient
from lib.config.Yaml import Yaml as Config
from lib.factory.StorageLocation import StorageLocation as DocFactory


config = Config('./config/config.yml').get('mongodb')
connection = MongoClient(config['host'], config['port'])

factory = DocFactory(config)


wiki = factory.wiki_collection()

wiki.drop_indexes()

wiki.create_index([('_id', 1)])
wiki.create_index([('code', 1)])
wiki.create_index([('name', 1)])
wiki.create_index([('admin_hierarchy', 1)])


gmaps = factory.gmaps_collection()

gmaps.drop_indexes()

gmaps.create_index([('_id', 1)])
gmaps.create_index([('code', 1)])
gmaps.create_index([('name', 1)])
gmaps.create_index([('admin_hierarchy', 1)])


insee = factory.insee_collection()

insee.drop_indexes()

insee.create_index([('_id', 1)])
insee.create_index([('code', 1)])
insee.create_index([('name', 1)])

istat = factory.istat_collection()

istat.drop_indexes()

insee.create_index([('_id', 1)])
insee.create_index([('code', 1)])
insee.create_index([('name', 1)])

internal = factory.internal_collection()

internal.drop_indexes()

internal.create_index([('_id', 1)])
internal.create_index([('code', 1)])
internal.create_index([('name', 1)])
internal.create_index([('admin_hierarchy', 1)])

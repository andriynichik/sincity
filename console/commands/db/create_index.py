from pymongo import MongoClient
from lib.config.Yaml import Yaml as Config
from lib.factory.StorageLocation import StorageLocation as DocFactory


config = Config('./config/config.yml').get('mongodb')
connection = MongoClient(config['host'], config['port'])

factory = DocFactory(config.get('mongodb'))

wiki = factory.wiki_collection()

wiki.drop_indexes()

wiki.create_index({'code': 1})
wiki.create_index({'name': 1})

gmaps = factory.gmaps_collection()

gmaps.drop_indexes()

gmaps.create_index({'code': 1})
gmaps.create_index({'name': 1})
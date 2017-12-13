from pymongo import MongoClient
import gridfs
from lib.config.Yaml import Yaml as Config
from pymongo import ReturnDocument
from pymongo import ReturnDocument
import sys

class Keygen:

	connection = MongoClient('wiki_parser_mongodb', 27017)
	db = connection.local	
	config = Config('./config/config.yml')

	def get_key_geocode(self):

		key =  self.db.keygen.find_one_and_update({'geocode': {'$lt': 2500}},
	     	{'$inc': {'geocode': 1}},
		    	projection={'key': True, '_id': False})
		try:
			return key['key']
		except Exception as e:
			return 'None geocode API KEY'

	def get_key_place(self):

		key =  self.db.keygen.find_one_and_update({'place': {'$lt': 1000}},
	     	{'$inc': {'place': 1}},
		    	projection={'key': True, '_id': False})
		try:
			return key['key']
		except Exception as e:
			return 'None place API KEY'


	@staticmethod
	def get_key_distance(self):

		key =  self.db.keygen.find_one_and_update({'distance': {'$lt': 2500}},
	     	{'$inc': {'distance': 1}},
		    	projection={'key': True, '_id': False})
		try:
			return key['key']
		except Exception as e:
			return 'None  distance API  KEY'

	@staticmethod
	def createGmapsKey(key):
		connection = MongoClient('wiki_parser_mongodb', 27017)
		db = connection.local
		data = {
			"key":key,
			"geocode":0,
			"place":0,
			"distance":0
		}
		post = db.keygen.find_one({'key': key})
		if post is None:
			result = db.keygen.insert_one(data)
			print("Created",key)
		else:
			print("KEY EXIST",key)
			
	@staticmethod
	def changeLimites():
		connection = MongoClient('wiki_parser_mongodb', 27017)
		db = connection.local
		db.test.update({}, {'$set': {'geocode': 0, "place":0, "distance":0}}, False, True)


Keygen = Keygen()
try:
	if sys.argv[1] == 'create':
		Keygen.createGmapsKey(str(sys.argv[2]))
	elif sys.argv[1] == 'cleen':
		Keygen.changeLimites()
except Exception as e:
	pass



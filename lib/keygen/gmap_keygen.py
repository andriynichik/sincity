from pymongo import MongoClient
import gridfs
from lib.config.Yaml import Yaml as Config
from pymongo import ReturnDocument
from pymongo import ReturnDocument
import sys

class Keygen:

	config = Config('./config/config.yml')
	mongo_config = config.get('mongodb')
	connection = MongoClient(mongo_config['host'], mongo_config['port'])

	def __init__(self):
		self.db = self.connection.local
	
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


	def get_key_distance(self):

		key =  self.db.keygen.find_one_and_update({'distance': {'$lt': 2500}},
	     	{'$inc': {'distance': 1}},
		    	projection={'key': True, '_id': False})
		try:
			return key['key']
		except Exception as e:
			return 'None  distance API  KEY'


	def createGmapsKey(key):
		data = {
			"key":key,
			"geocode":0,
			"place":0,
			"distance":0
		}
		post = self.db.keygen.find_one({'key': key})
		if post is None:
			result = self.db.keygen.insert_one(data)
			print("Created",key)
		else:
			print("KEY EXIST",key)
			

	def changeLimites(self):

		self.db.update({}, {'$set': {'geocode': 0, "place":0, "distance":0}}, False, True)


if __name__ == '__main__':
    Keygen = Keygen()
    if sys.argv[1] == 'create':
    	Keygen.createGmapsKey(str(sys.argv[2]))
    elif sys.argv[1] == 'cleen':
    	Keygen.changeLimites()
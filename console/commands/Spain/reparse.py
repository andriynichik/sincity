from pymongo import MongoClient

class ReParse():

	def __init__(self, mongoId):
		super(ReParse, self).__init__()
		self.mongoId = mongoId

	def run(self, mongoId):
		pass

	def by_goecode(self):
		pass

	def by_placeId(self):
		pass

# if __name__ == '__main__':
#     ReParse = ReParse()
#     if sys.argv[1] == 'create':
#     	ReParse.createGmapsKey(str(sys.argv[2]))
#     elif sys.argv[1] == 'cleen':
#     	ReParse.changeLimites()
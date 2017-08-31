from lib.logger.Log import Log
from time import time
from pymongo import MongoClient


class MongoDB(Log):

    def __init__(self, log_name, config):
        connection = MongoClient(config['host'], config['port'])
        self.collection = connection.log[log_name]

    def add(self, message, type=Log.WARNING):
        data = {
            'time': time(),
            'type': type,
            'message': message
        }
        self.collection.insert_one(data)

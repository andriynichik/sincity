from lib.logger.Log import Log
from time import time
from pymongo import MongoClient


class MongoDB(Log):
    STATUS_NEW = 1
    STATUS_CLOSE = 2

    def __init__(self, log_name, config):
        connection = MongoClient(config['host'], config['port'])
        self._storage = connection.log[log_name]

    def add(self, message, type=Log.WARNING):
        data = {
            'time': time(),
            'status': self.STATUS_NEW,
            'type': type,
            'message': message
        }
        self._storage.insert_one(data)

    def close(self, id):
        return self._storage.update_one({'_id': id}, {'$set': {'status': self.STATUS_CLOSE}}).acknowledged

from pymongo import MongoClient

from lib.hashlib.sha512 import sha512


class RecursiveParser:

    def __init__(self, name, config):
        connection = MongoClient(config['host'], config['port'])
        self.parsed_page_collection = connection.parsed_page[name]
        self.url_pool_collection = connection.url_pool[name]
        self.hash_lib = sha512()

    def is_page_parsed(self, url):
        return bool(self.parsed_page_collection.count({'code': self._hash(url)}))

    def page_parsed(self, url):
        doc = {'code': self._hash(url), 'url': url}
        self.parsed_page_collection.insert_one(doc)

    def get_next(self):
        doc = self.url_pool_collection.find_one({})
        return doc if doc else None

    def is_url_in_pool(self, url):
        return bool(self.url_pool_collection.count({'code': self._hash(url)}))


    def add_url_to_pool(self, url, level, from_url):
        code = self._hash(url)
        doc = {'code': code, 'url': url, 'level': level, 'from_url': from_url}
        self.url_pool_collection.insert_one(doc)

    def remove_from_pool(self, url):
        code = self._hash(url)
        result = self.url_pool_collection.delete_one({'code': code})
        return result.deleted_count

    def _hash(self, url):
        return self.hash_lib.make(url)
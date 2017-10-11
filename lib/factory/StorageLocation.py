from lib.hashlib.sha512 import sha512
from pymongo import MongoClient
from lib.location.Wiki import Wiki
from lib.location.Insee import Insee
from lib.location.GMap import GMap
from lib.location.Internal import Internal


class StorageLocation:

    def __init__(self, storage_config):
        self._hash_lib = sha512()
        connection = MongoClient(storage_config['host'], storage_config['port'])
        self._db = connection.location

    def wiki(self, url):
        code = self._hash_lib.make(url)
        return Wiki(code=code, storage=self._db)

    def gmaps(self, code):
        return GMap(code=code, storage=self._db)

    def insee(self, code):
        return Insee(code=code, storage=self._db)

    def internal(self, code):
        return Internal(code, storage=self._db)

    def gmaps_collection(self):
        return self._db[GMap.TYPE]

    def wiki_collection(self):
        return self._db[Wiki.TYPE]

    def insee_collection(self):
        return self._db[Insee.TYPE]

    def internal_collection(self):
        return self._db[Internal.TYPE]

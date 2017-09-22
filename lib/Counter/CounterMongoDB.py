from lib.Counter.Counter import Counter


class CounterMongoDB(Counter):

    def __init__(self, start, end, counter_name, connection, step=1, ttl=86400):
        super(CounterMongoDB, self).__init__(start=start, end=end, step=step, ttl=ttl)
        self._query = {'name': counter_name}
        self._storage = connection.counters.counter
        self.get_document()

    def get_document(self):
        document = self._storage.find_one(self._query)
        if not document:
            doc = {
                'name': self._query.get('name'),
                'current': self.current,
                'start_time': self.start_time
            }
            self._storage.insert_one(doc)
            document = self._storage.find_one(self._query)

        return document

    def get_current(self):
        doc = self.get_document()
        return doc.get('current')

    def set_current(self, val):
        self._storage.update_one(self._query, {'$set': {'current': val}})

    def get_start_time(self):
        doc = self.get_document()
        return doc.get('start_time')

    def set_start_time(self, val):
        self._storage.update_one(self._query, {'$set': {'start_time': val}})

    def step(self):
        self._storage.update_one(self._query, {'$inc': {'current': self.one_step}})
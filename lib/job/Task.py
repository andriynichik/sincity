class Task:
    def __init__(self, options, storage, log):
        self._options = options
        self._storage = storage
        self._log = log

    def mark_as_complete(self):
        self._storage.as_complete(self._options.id)

    def execute(self):
        pass
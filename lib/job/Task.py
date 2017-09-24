class Task:

    TYPE = 'task'

    def __init__(self, options, storage, log):
        self._options = options
        self._storage = storage
        self._log = log

    @staticmethod
    def get_name(name):
        return '{}_{}'.format(Task.TYPE, name)

    def mark_as_complete(self):
        self._storage.as_complete(self._options.get('id'))

    def execute(self):
        pass

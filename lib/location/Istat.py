from lib.location.External import External


class Istat(External):

    TYPE = 'istat'

    def __init__(self, code, storage):
        super(Istat, self).__init__(code, storage=storage, type=self.TYPE)
from lib.location.External import External


class Insee(External):

    TYPE = 'insee'

    def __init__(self, code, storage):
        super(Insee, self).__init__(code, storage=storage, type=self.TYPE)
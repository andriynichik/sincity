from lib.logger.Log import Log
from time import time


class File(Log):

    def __init__(self, file_name):
        self._fh = open(file_name, 'a+')

    def add(self, message, type=Log.WARNING):
        message = "[{time}][{type}] {message}\n".format(time=time(), type=type, message=str(message))
        self._fh.write(message)

    def __del__(self):
        self._fh.close()
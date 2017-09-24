from lib.parser.map.google.France import France
from lib.parser.map.google.Italy import Italy


class GMapFactory:

    @staticmethod
    def france(response):
        objects = []
        for point in response:
            objects.append(France(point))
        return objects


    @staticmethod
    def italy(response):
        objects = []
        for point in response:
            objects.append(Italy(point))
        return objects
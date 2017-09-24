from geopy.distance import vincenty
import matplotlib.path as MplPath


class Comparison:

    @staticmethod
    def by_name(original, candidate):
        pass

    @staticmethod
    def by_distance(original, candidate):
        return vincenty((original.get('lat'), original.get('lng')), (candidate.get('lat'), candidate.get('lng'))).meters

    @staticmethod
    def by_admin_hierarchy(original, candidate):
        pass

    @staticmethod
    def by_polygon(polygon, candidate):
        """
        :param polygon: [(lat1, lng1), (lat2, lng2), (lat3, lng3), (lat1, lng1)]
        :param candidate:
        :return:
        """
        path = MplPath.Path(polygon)
        return path.contains_point((candidate.get('lat'), candidate.get('lng')))
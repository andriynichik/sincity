from lib.compare.converter.Converter import Converter

class GMap(Converter):
    def __init__(self, obj):
        super(GMap, self).__init__(obj)
        self._admin_levels= {}
        for i in range(1, 14):
            attr_name = 'ADMIN_LEVEL_{}'.format(i)
            if hasattr(obj, attr_name):
                self._admin_levels.set[getattr(obj, attr_name)] = i

    def by_name(self):
        dic = {'en': self.obj.name}
        return dic

    def _admin_value(self, value):
        dic = {'en': value.get('name')}
        return dic

    def by_admin_hierarchy(self):
        pass

    def by_distance(self):
        pass
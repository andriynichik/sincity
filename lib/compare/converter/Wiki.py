import lib.compare.converter.Converter as Converter

class Wiki(Converter):

    def __init__(self, obj):
        super(Wiki, self).__init__(obj)
        self._admin_levels= {}
        for i in range(1, 14):
            attr_name = 'ADMIN_LEVEL_{}'.format(i)
            if hasattr(obj, attr_name):
                self._admin_levels.set[getattr(obj, attr_name)] = i

    def by_name(self):
        dic = {'origin': self.obj.get('name')}
        for key, value in self.obj.get('i18n', {}).items():
            dic[key] = value.get('name')
        return dic

    def by_distance(self):
        return {'lat': self.obj.get('center', {}).get('lat'), 'lng': self.obj.get('center', {}).get('lng')}

    def _admin_value(self, value):
        dic = {'origin': value.get('name')}
        return dic

    def by_admin_hierarchy(self):
        admins = {}
        for key, value in self.obj.get('admin_hierarchy'):
            admins[self._admin_index(value)] = self._admin_value(value)

        return admins

    def by_polygon(self):
        return self.by_distance()
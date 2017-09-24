class Converter:

    def __init__(self, obj):
        self.obj = obj

    def by_name(self):
        pass

    def by_admin_hierarchy(self):
        pass

    def by_distance(self):
        pass

    def _admin_index(self, value):
        return self._admin_levels[value.get('type')]
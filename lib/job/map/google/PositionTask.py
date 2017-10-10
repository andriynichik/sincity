from lib.job.map.google.MapTask import MapTask
import sys


class PositionTask(MapTask):

    TYPE = 'gmap_position'

    @staticmethod
    def get_name(name):
        return '{}_{}'.format(PositionTask.TYPE, name)

    def execute(self):
        try:
            latitude = self._options.get('request').get('lat')
            longitude = self._options.get('request').get('lng')
            loader = self._options.get('loader')
            doc_factory = self._options.get('doc_factory')
            force_update = self._options.get('force_update')
            parser = self._options.get('parser')

            position_content = loader.by_position(lat=latitude, lng=longitude)
            for obj in position_content:
                obj = parser(obj)
                code = obj.get_place_id()
                if obj.get_place_id():
                    doc = doc_factory.gmaps(code)
                    if doc.is_new() or force_update:
                        dic = obj.as_dictionary()
                        if dic.get('type'):
                            doc.update(dic)
                    self.update_meta(request=(latitude, longitude), document=doc)
        except:
            self._log.add("{} {}".format(self._options.get('request'), sys.exc_info()[0]))

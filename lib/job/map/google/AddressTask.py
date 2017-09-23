from lib.job.map.google.MapTask import MapTask


class AddressTask(MapTask):

    TYPE = 'gmap_address'

    @staticmethod
    def get_name(name):
        return '{}_{}'.format(AddressTask.TYPE, name)

    def execute(self):

        address = self._options.get('request')
        loader = self._options.get('loader')
        doc_factory = self._options.get('doc_factory')
        force_update = self._options.get('force_update')
        parser = self._options.get('parser')

        address_content = loader.by_address(address=address)
        for obj in address_content:
            obj = parser(obj)
            code = obj.get_place_id()
            if obj.get_place_id():
                doc = doc_factory.gmaps(code)
                if doc.is_new() or force_update:
                    dic = obj.as_dictionary()
                    if dic.get('type'):
                        doc.update(dic)
                self.update_meta(request=address, document=doc)

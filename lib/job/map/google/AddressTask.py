from lib.job.map.google.MapTask import MapTask


class AddressTask(MapTask):

    def execute(self):

        address = self._options.address
        loader = self._options.loader
        doc_factory = self._options.doc_factory
        force_update = self._options.force_update
        parser = self._options.parser

        address_content = loader.by_address(address=address)
        objects = parser(address_content)
        for object in objects:
            code = object.get_place_id()
            if object.get_place_id():
                doc = doc_factory.gmaps(code)
                if doc.is_new() or force_update:
                    doc.update(object.as_dictionary())
                self.update_meta(request=address, document=doc)
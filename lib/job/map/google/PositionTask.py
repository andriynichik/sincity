from lib.job.map.google.MapTask import MapTask


class PositionTask(MapTask):

    def execute(self):

        latitude = self._options.lat
        longitude = self._options.lng
        loader = self._options.loader
        doc_factory = self._options.doc_factory
        force_update = self._options.force_update
        parser = self._options.parser

        position_content = loader.by_position(lat=latitude, lng=longitude)
        objects = parser(position_content)
        for object in objects:
            code = object.get_place_id()
            if object.get_place_id():
                doc = doc_factory.gmaps(code)
                if doc.is_new() or force_update:
                    doc.update(object.as_dictionary())
                self.update_meta(request=(latitude, longitude), document=doc)
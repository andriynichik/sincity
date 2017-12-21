class Spider:

    def __init__(self, loader_factory, gmap_parser, wiki_parser, doc_factory, language, config, use_cache=True):
        self.use_cache=use_cache
        self.config = config
        self.language = language
        self.loader_factory = loader_factory
        self.gmap_loader = self._gmap_loader()
        self.wiki_loader = self._wiki_loader()
        self.gmap_parser = gmap_parser
        self.wiki_parser = wiki_parser
        self.doc_factory = doc_factory

    def get_gmap_address(self, address):
        raw = self.gmap_loader.by_address(address=address, use_cache=self.use_cache)
        return self._gmap_documents(raw=raw, request=address)

    def get_gmap_position(self, lat, lng):
        raw = self.gmap_loader.by_position(lat=lat, lng=lng, use_cache=self.use_cache)
        return self._gmap_documents(raw=raw, request=(lat, lng))

    def get_gmap_place_id(self, place_id):
        raw = self.gmap_loader.by_place_id(place_id=place_id, use_cache=self.use_cache)
        return self._gmap_documents(raw=raw, request=place_id)

    def get_by_places_by_type(self, address,  placeName, myPlaceTypes):
        raw = self.gmap_loader.by_places(address=address, use_cache=self.use_cache)
        objects = self.gmap_parser(raw)
        for objects_item in objects:
            if objects_item.get_places_type() in myPlaceTypes and objects_item.get_places_name().strip() == placeName.strip():
                    return objects_item.get_places_PlaceId()
        return None
        

    def get_wiki_url(self, url):
        wiki_content, code = self.wiki_loader.load(url, headers={'User-Agent': 'Mozilla/5.0'})
        wiki_parser = self.wiki_parser(wiki_content)
        if wiki_parser.is_many_answers():
            return wiki_parser.get_answers_links()
        else:
            doc = self.doc_factory.wiki(url)
            dict = wiki_parser.as_dictionary()
            dict.update(url=url)
            doc.update(dict)
            self._update_meta(document=doc, request=url)
            return doc

    def _gmap_documents(self, raw, request):
        objects = self.gmap_parser(raw)
        documents = []
        for obj in objects:
            code = obj.get_place_id()
            if obj.get_place_id():
                doc = self.doc_factory.gmaps(code)
                dic = obj.as_dictionary()
                if dic.get('type'):
                    doc.update(dic)
                self._update_meta(document=doc, request=request)
                documents.append(doc)

        return documents

    def _gmap_loader(self):
        gmap_config = self.config.get('googlemaps')
        gmap_config.update(language=self.language)
        return self.loader_factory.loader_gmaps_with_cache(gmaps_config=gmap_config, storage_config=self.config.get('mongodb'))

    def _wiki_loader(self):
        return self.loader_factory.loader_with_mongodb(storage_config=self.config.get('mongodb'))

    @staticmethod
    def _update_meta(document, request):
        actual_doc = document.get_document()
        added_requests = [(tuple(x) if isinstance(x, list) else x) for x in actual_doc.get('requests', ())]
        added_requests.append(request)
        actual_doc.update(requests=list(set(added_requests)))
        document.update(actual_doc)
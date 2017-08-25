from lib.job.wiki.WikiTask import WikiTask


class RequestTask(WikiTask):

    def execute(self):

        url = self._options.url_format.format(self._options.request)
        loader = self._options.loader
        parser = self._options.parser
        doc_factory = self._options.doc_factory
        force_update = self._options.force_update
        headers = self._options.headers

        content, code = loader.load(url, headers=headers)
        parsed_page = parser(content)
        if parsed_page.is_many_answers():
            urls = parsed_page.get_answers_links()
            for answer_url in urls:
                doc = doc_factory.wiki(answer_url)
                if doc.is_new() or force_update:
                    page, code = loader.load(answer_url, headers=headers)
                    page_parser = parser(page)
                    if page_parser.is_location_page():
                        doc.update(page_parser.as_dictionary())
                self.update_meta(url=answer_url, request=url, document=doc)
        elif parser.is_location_page():
            doc = doc_factory.wiki(url)
            if doc.is_new() or force_update:
                doc.update(parser.as_dictionary())
            self.update_meta(url=url, request=url, document=doc)

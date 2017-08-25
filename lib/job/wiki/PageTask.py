from lib.job.wiki.WikiTask import WikiTask


class PageTask(WikiTask):

    def execute(self):

        loader = self._options.loader
        parser = self._options.parser
        force_update = self._options.force_update
        link = self._options.link
        headers = self._options.headers
        document_factory= self._options.document_factory

        content, code = loader.load(link, headers=headers)
        parsed_page = parser(content)

        if parsed_page.is_many_answers():
            urls = parsed_page.get_answers_links()
            for url in urls:
                doc = document_factory.wiki(url)
                if doc.is_new() or force_update:
                    page, code = loader.load(url, headers=headers)
                    page_parser = parser(page)
                    if page_parser.is_location_page():
                        doc.update(page_parser.as_dictionary())
                self.update_meta(url=url, request=link, document=doc)
        elif parsed_page.is_location_page():
            doc = document_factory.wiki(link)
            if doc.is_new() or force_update:
                doc.update(parsed_page.as_dictionary())
            self.update_meta(url=link, request=link, document=doc)
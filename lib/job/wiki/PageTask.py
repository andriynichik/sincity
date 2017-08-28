from lib.job.wiki.WikiTask import WikiTask


class PageTask(WikiTask):

    TYPE = 'wiki_page'

    def execute(self):
        force_update = self._options.force_update
        link = self._options.request

        content, code = self.loader.load(link, headers=self.headers)
        parsed_page = self.parser(content)

        if parsed_page.is_many_answers():
            urls = parsed_page.get_answers_links()
            for url in urls:
                doc = self.document_factory.wiki(url)
                if doc.is_new() or force_update:
                    page, code = self.loader.load(url, headers=self.headers)
                    page_parser = self.parser(page)
                    if page_parser.is_location_page():
                        doc.update(page_parser.as_dictionary())
                self.update_meta(url=url, request=link, document=doc)
        elif parsed_page.is_location_page():
            doc = self.document_factory.wiki(link)
            if doc.is_new() or force_update:
                doc.update(parsed_page.as_dictionary())
            self.update_meta(url=link, request=link, document=doc)
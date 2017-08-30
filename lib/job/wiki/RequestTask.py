from lib.job.wiki.WikiTask import WikiTask


class RequestTask(WikiTask):

    TYPE = 'wiki_request'

    def execute(self):
        url = self._options.get('url_format').format(self._options.get('request'))
        force_update = self._options.get('force_update')
        content, code = self.loader.load(url, headers=self.headers)
        parsed_page = self.parser(content)
        if parsed_page.is_many_answers():
            urls = parsed_page.get_answers_links()
            for answer_url in urls:
                doc = self.document_factory.wiki(answer_url)
                if doc.is_new() or force_update:
                    page, code = self.loader.load(answer_url, headers=self.headers)
                    page_parser = self.parser(page)
                    if page_parser.is_location_page():
                        doc.update(page_parser.as_dictionary())
                self.update_meta(url=answer_url, request=url, document=doc)
        elif parsed_page.is_location_page():
            doc = self.document_factory.wiki(url)
            if doc.is_new() or force_update:
                doc.update(parsed_page.as_dictionary())
            self.update_meta(url=url, request=url, document=doc)

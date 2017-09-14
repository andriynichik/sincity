import re
from lib.job.wiki.WikiTask import WikiTask


class PageRecursiveTask(WikiTask):

    TYPE = 'wiki_page_recursive'

    def __init__(self, options, storage, log):
        super(PageRecursiveTask, self).__init__(options=options, storage=storage, log=log)
        self.link = self._options.request
        self.page_parsed = []
        self.url_pool = [self.link]
        self.host = self._options.host

    def execute(self):
        force_update = self._options.force_update
        for link in self.url_pool:
            try:
                content, code = self.loader.load(link, headers=self.headers)
                parsed_page = self.parser(content)
                if parsed_page.is_many_answers():
                    urls = parsed_page.get_answers_links()
                    for url in urls:
                        self._add_link_to_pool(url)
                elif parsed_page.is_location_page():
                    doc = self.document_factory.wiki(self.link)
                    if doc.is_new() or force_update:
                        doc.update(parsed_page.as_dictionary())
                    self.update_meta(url=link, request=link, document=doc)
                    links_on_page = parsed_page.get_all_links()
                    for link_on_page in links_on_page:
                        if self._is_correct_link(link_on_page):
                            self._add_link_to_pool(self.host + link_on_page)
                self._page_parsed(link)
            except:
                self._page_parsed(link)

    def _is_correct_link(self, link):
        result = re.search(r'^/wiki/', link)

        return True if result else False

    def _add_link_to_pool(self, link):
        if not (link in self.page_parsed):
            self.url_pool.append(link)

    def _page_parsed(self, link):
        self.page_parsed.append(link)
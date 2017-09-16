import re
from lib.job.wiki.WikiTask import WikiTask
import sys


class PageRecursiveTask(WikiTask):

    TYPE = 'wiki_page_recursive'

    def __init__(self, options, storage, log):
        super(PageRecursiveTask, self).__init__(options=options, storage=storage, log=log)
        self.link = self._options.get('request').get('link')
        self.max_level = self._options.get('request').get('level', 1)
        self.host = self._options.get('host')
        self.page_parsed = []
        self.url_pool = [(1, self.link, '')]

    def execute(self):
        force_update = self._options.get('force_update')
        for level, link, from_link in self.url_pool:
            try:
                content, code = self.loader.load(link, headers=self.headers)
                parsed_page = self.parser(content)
                if parsed_page.is_many_answers():
                    urls = parsed_page.get_answers_links()
                    for url in urls:
                        self._add_link_to_pool(url, link)
                elif parsed_page.is_location_page():
                    doc = self.document_factory.wiki(self.link)
                    if doc.is_new() or force_update:
                        doc.update(parsed_page.as_dictionary())
                    self.update_meta(url=link, request=link, document=doc)
                    links_on_page = parsed_page.get_all_links()
                    for link_on_page in links_on_page:
                        if self._is_correct_link(link_on_page):
                            self._add_link_to_pool(link_on_page, link)
                elif self.max_level >= level:
                    links_on_page = parsed_page.get_all_links()
                    for link_on_page in links_on_page:
                        if self._is_correct_link(link_on_page):
                            self._add_link_to_pool(link_on_page, link, level + 1)
                self._page_parsed(link)
            except:
                errors = sys.exc_info()
                self._log.add(str(errors))
                self._page_parsed(link)

    def _is_correct_link(self, link):
        result = re.search(r'/' + re.escape(self.host) + r'/wiki/', link)
        return True if result else False

    def _add_link_to_pool(self, link, from_link, level=1):
        if not (link in self.page_parsed):
            self.url_pool.append((level, link, from_link))

    def _page_parsed(self, link):
        self.page_parsed.append(link)
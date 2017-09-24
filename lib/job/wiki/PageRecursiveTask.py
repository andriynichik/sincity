import re
from lib.job.wiki.WikiTask import WikiTask
import sys


class PageRecursiveTask(WikiTask):

    TYPE = 'wiki_page_recursive'

    @staticmethod
    def get_name(name):
        return '{}_{}'.format(PageRecursiveTask.TYPE, name)

    def __init__(self, options, storage, log):
        super(PageRecursiveTask, self).__init__(options=options, storage=storage, log=log)
        self.recursive_storage = self._options.get('recursive_storage')
        self.link = self._options.get('request').get('link')
        self.max_level = self._options.get('request').get('level', 1)
        self.host = self._options.get('host')
        self.log_history = self._options.get('log_history')
        self._add_link_to_pool(self.link, '', 1)

    def execute(self):
        force_update = self._options.get('force_update')
        doc = self.recursive_storage.get_next()
        while doc:
            level = doc.get('level')
            link = doc.get('url')
            from_link = doc.get('from_url')
            self.log_history.add('[{}] {}\t{}\t{}'.format('begin', level, link, from_link))
            try:
                content, code = self.loader.load(link, headers=self.headers)
                parsed_page = self.parser(content)
                if parsed_page.is_many_answers():
                    self.log_history.add('[{}] {} {}'.format('is_many_answers', code, link))
                    urls = parsed_page.get_answers_links()
                    for url in urls:
                        self._add_link_to_pool(url, link)
                elif parsed_page.is_location_page():
                    self.log_history.add('[{}] {} {}'.format('is_location_page', code, link))
                    doc = self.document_factory.wiki(link)
                    if doc.is_new() or force_update:
                        doc.update(parsed_page.as_dictionary())
                    self.update_meta(url=link, request=link, document=doc)
                    links_on_page = parsed_page.get_all_links()
                    for link_on_page in links_on_page:
                        if self._is_correct_link(link_on_page):
                            self._add_link_to_pool(link_on_page, link)
                elif self.max_level >= level:
                    self.log_history.add('[{}] {} {}'.format('intermediate_page', code, link))
                    links_on_page = parsed_page.get_all_links()
                    for link_on_page in links_on_page:
                        if self._is_correct_link(link_on_page):
                            self._add_link_to_pool(link_on_page, link, level + 1)
                self._page_parsed(link)
            except:
                self.log_history.add('[{}] {}'.format('error_page', link))
                errors = sys.exc_info()
                self._log.add('[{}] | {}'.format(link, str(errors)))
                self._page_parsed(link)
            doc = self.recursive_storage.get_next()

    def _is_correct_link(self, link):
        result = re.search(r'/' + re.escape(self.host) + r'/wiki/', link)
        return True if result else False

    def _add_link_to_pool(self, link, from_link, level=1):
        in_parsed = self.recursive_storage.is_page_parsed(url=link)
        in_pool = self.recursive_storage.is_url_in_pool(url=link)
        if not in_parsed and not in_pool:
            self.recursive_storage.add_url_to_pool(url=link, level=level, from_url=from_link)

    def _page_parsed(self, url):
        self.recursive_storage.page_parsed(url=url)
        self.recursive_storage.remove_from_pool(url=url)
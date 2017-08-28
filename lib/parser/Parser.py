import re
import html
import urllib.parse
from bs4 import BeautifulSoup


class Parser:

    BEAUTIFULSOUP_PARSER = "html.parser"

    def __init__(self, content):
        self.content = content.decode('utf-8')
        self._content_soap = BeautifulSoup(self.content, self.BEAUTIFULSOUP_PARSER)

    def as_dictionary(self):
        pass

    @staticmethod
    def replace_html(content):
        result = re.sub('<[^>]*>', ' ', content)
        result = html.unescape(result)
        result = re.sub('\s+', ' ', result)
        return result.strip()

    @staticmethod
    def _get_first(list_of_data, default=''):
        try:
            if list_of_data:
                iterator = iter(list_of_data)
                for item in list_of_data:
                    return item
        except TypeError:
            pass
        return default

    @staticmethod
    def _url_decode(content):
        return urllib.parse.unquote(content)

    def get_all_links(self):
        soup = self._content_soap.findAll('a', href=True)
        return [(lambda x: x['href'])(x) for x in soup]
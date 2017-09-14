from lib.factory.Loader import Loader as LoaderFactory
from lib.parser.wiki.Wiki import Wiki as WikiParser

loader = LoaderFactory.loader()

url = 'https://it.wikipedia.org/wiki/Roma'
headers = {'User-Agent': 'Mozilla/5.0'}

page, code = loader.load(url, headers)

parser = WikiParser(page)

print(parser.get_all_links())
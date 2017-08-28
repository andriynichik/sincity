from lib.parser.Parser import Parser
from lib.factory.Loader import Loader as Factory


loader = Factory.loader()

url = 'https://fr.wikipedia.org/wiki/Paris'
headers = {'User-Agent': 'Mozilla/5.0'}

content, code = loader.load(url, headers=headers)

parser = Parser(content)

links = parser.get_all_links()

print(links)


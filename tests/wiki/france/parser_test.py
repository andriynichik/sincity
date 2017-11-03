from lib.factory.Loader import Loader as Factory
import sys
from lib.config.Yaml import Yaml as Config
from lib.parser.wiki.France import France as WikiParser


config = Config('./config/config.yml')

loader = Factory.loader_with_mongodb(config.get('mongodb'))

url = 'https://fr.wikipedia.org/wiki/Occitanie_(r%C3%A9gion_administrative)'
headers = {'User-Agent': 'Mozilla/5.0'}

content, code = loader.load(url, headers=headers)

content = loader.from_cache(url, headers=headers)

if code == 200 and len(content) > 0:
    print('.')
else:
    print('E')
    sys.exit()

#print(content)

parser = WikiParser(content)

dic = parser.as_dictionary()

print('is location: {}'.format(('yes' if parser.is_location_page() else 'no')))
print('is list: {}'.format(('yes' if parser.is_many_answers() else 'no')))

dic.pop('i18n', None)

print(dic)
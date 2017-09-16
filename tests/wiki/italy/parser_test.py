from lib.factory.Loader import Loader as Factory
import sys
from lib.config.Yaml import Yaml as Config
from lib.parser.wiki.Italy import Italy as WikiParser


config = Config('./config/config.yml')

loader = Factory.loader_with_mongodb(config.get('mongodb'))

url = 'https://it.wikipedia.org/wiki/Variazioni_amministrative_della_Calabria'
headers = {'User-Agent': 'Mozilla/5.0'}

content, code = loader.load(url, headers=headers)

content = loader.from_cache(url, headers=headers)

if code == 200 and len(content) > 0:
    print('.')
else:
    print('E')
    sys.exit()


parser = WikiParser(content)

dic = parser.as_dictionary()

print('is location: {}'.format(('yes' if parser.is_location_page() else 'no')))
print('is list: {}'.format(('yes' if parser.is_many_answers() else 'no')))

print(dic)
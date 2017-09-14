from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.factory.Loader import Loader as LoaderFactory
from lib.config.Yaml import Yaml as Config
from lib.parser.wiki.Italy import Italy as WikiParser


config = Config('./config/config.yml')
document_factory = DocFactory(config.get('mongodb'))

url = 'https://it.wikipedia.org/wiki/Roma'
headers = {'User-Agent': 'Mozilla/5.0'}

loader = LoaderFactory.loader_with_mongodb(config.get('mongodb'))

content, code = loader.load(url, headers=headers)

parser = WikiParser(content)

doc = document_factory.wiki(url)

print('.' if doc.is_new() else 'E', end='')

document = doc.get_document()

print('.' if 'code' in document else 'E', end='')

doc.update(parser.as_dictionary())

dic = doc.get_document()

print('.' if dic.get('name') == 'Roma' else 'E', end='')
print('.' if dic.get('type') == 'comune' else 'E', end='')
print('.' if len(dic.get('admin_hierarchy')) == 3 else 'E', end='')
print('.' if dic.get('admin_hierarchy')[0].get('name') == 'Italia' else 'E', end='')
print('.' if dic.get('admin_hierarchy')[0].get('type') == parser.ADMIN_LEVEL_1 else 'E', end='')
print('.' if dic.get('admin_hierarchy')[1].get('type') == parser.ADMIN_LEVEL_2 else 'E', end='')
print('.' if len(dic.get('i18n')) > 0 else 'E', end='')
print('.' if dic.get('i18n').get('en').get('name') == 'Rome'  else 'E', end='')
print('.' if dic.get('center').get('lat') else 'E', end='')
print('.' if dic.get('center').get('lng') else 'E', end='')
print('.' if dic.get('altitude') else 'E', end='')
print('.' if dic.get('population') > 0 else 'E', end='')
print('.' if dic.get('density') > 0 else 'E', end='')
print('.' if dic.get('area') > 0 else 'E', end='')
print('.' if len(dic.get('postal_codes')) > 0 else 'E', end='')



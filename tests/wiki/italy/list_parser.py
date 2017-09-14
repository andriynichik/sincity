from lib.factory.Loader import Loader as Factory
from lib.parser.wiki.Italy import Italy as WikiFr

loader = Factory.loader()

url = 'https://it.wikipedia.org/w/index.php?search=Italia,Roma&title=Sp%C3%A9cial:Recherche&profile=default&fulltext=1&searchengineselect=mediawiki&searchToken=7uw18iziltcdfvvdo87qvyxu8'
headers = {'User-Agent': 'Mozilla/5.0'}

content, code = loader.load(url, headers=headers)

parser = WikiFr(content)

print('.' if parser.is_many_answers() else 'E', end='')

print('.' if parser.get_answers_links() else 'E', end='')
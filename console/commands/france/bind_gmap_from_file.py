from DataStructure.DataWiki import parser_wiki
from DataStructure.DataGMap import parser_gmap
from DataStructure.DataInsee import parser_insee
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.config.Yaml import Yaml as Config
from lib.hashlib.sha512 import sha512 as hash
from lib.parser.wiki.France import France as ParserFranceWiki
from lib.factory.Loader import Loader as LoaderFactory
import csv
from lib.parser.map.google.GMapFactory import GMapFactory as MapFactory
from lib.spider.Spider import Spider


files = [
    #'data/france/Departements_28_08_17_cards.csv',
    #'data/france/arrondissements_25_08_17_cards.csv',
    'data/france/20_08_17_canton_google_3.csv',
    'data/france/communes_17_09_17.csv'
]

config = Config('./config/config.yml')

doc_factory = DocFactory(config.get('mongodb'))
language='fr'

spider = Spider(
    loader_factory=LoaderFactory,
    gmap_parser=MapFactory.france,
    wiki_parser=ParserFranceWiki,
    doc_factory=doc_factory,
    language=language,
    config=config,
    use_cache=True
)

internal_collection = doc_factory.internal_collection()
i = 0
for csv_file in files:
    with open(csv_file, encoding='utf-8') as admin_div_CSV:
        for line in csv.DictReader(admin_div_CSV, delimiter='\t'):
            try:
                i = i + 1
                print(i)
                dct = {}
                wiki_parsed = {}
                wiki = parser_wiki(line)

                gmap = parser_gmap(line)
                wiki_obj = doc_factory.wiki(wiki.get('url'))

                if gmap.get('code'):
                    code = gmap.get('code')
                elif gmap:
                    code = hash().make(str(gmap))
                else:
                    code = 'dummy'

                gmap_obj = doc_factory.gmaps(code)
                gmap.update(code=code)
                gmap_obj.update(gmap)

                wiki_code = wiki_obj.get_document().get('code')

                doc = internal_collection.find_one({'source.wiki': wiki_code})

                if doc and doc.get('code'):
                    doc_obj = doc_factory.internal(doc.get('code'))
                    source = doc_obj.get_document().get('source')
                    source.update(gmap=gmap_obj.get_document().get('code'))
                    print(gmap_obj.get_document().get('code'))

                    doc_obj.update({'source': source})

            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                print('Error')
                print(line)
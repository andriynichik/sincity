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
    'data/france/Departements_28_08_17_cards.csv',
    'data/france/arrondissements_25_08_17_cards.csv',
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


def gmap_by_address(wiki):

    address = []
    for name, value in wiki.get('admin_hierarchy', {}).items():
        address.append(value.get('name'))
    address.append(wiki.get('name'))

    objects = spider.get_gmap_address(','.join(address))

    gmap = {}
    if objects:
        gmap = objects[0].get_document()
        gmap.update(language=spider.gmap_loader._language)

    return gmap


def make_internal(insee, insee_obj, wiki, wiki_obj, gmap, gmap_obj):
    internal = {}

    if gmap.get('name'):
        internal.update(name=gmap.get('name'))
    elif wiki.get('name'):
        internal.update(name=wiki.get('name'))

    if wiki.get('admin_hierarchy', {}):
        for level in range(1, 12):
            if not wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_{}'.format(level)):
                internal.update(type='ADMIN_LEVEL_{}'.format(level))
                break
    elif gmap.get('admin_hierarchy', {}):
        for level in range(1, 12):
            if not gmap.get('admin_hierarchy', {}).get('ADMIN_LEVEL_{}'.format(level)):
                internal.update(type='ADMIN_LEVEL_{}'.format(level))
                break
    elif wiki.get('type'):
        internal.update(type=wiki.get('type'))
    elif gmap.get('type'):
        internal.update(type=gmap.get('type'))

    languages = {}
    for lang, i18n in wiki.get('i18n', {}).items():
        languages.update({lang: i18n.get('name')})
    internal.update(i18n=languages)

    if gmap.get('name'):
        if gmap.get('language') == 'fr':
            internal.get('i18n', {}).update(fr=gmap.get('name'))
        elif gmap.get('language') == 'en':
            internal.get('i18n', {}).update(en=gmap.get('name'))

    if wiki.get('admin_hierarchy'):
        internal.update(admin_hierarchy=wiki.get('admin_hierarchy', {}))

    if wiki.get('capital'):
        internal.update(capital=wiki.get('capital', {}).get('name'))

    if wiki.get('center'):
        internal.update(center=wiki.get('center'))
    elif gmap.get('center'):
        internal.update(center=gmap.get('center'))

    if gmap.get('bounds'):
        internal.update(bounds=gmap.get('bounds'))

    if wiki.get('altitude'):
        internal.update(altitude=wiki.get('altitude'))

    if wiki.get('population'):
        internal.update(population=wiki.get('population'))
    elif insee.get('InseeXls_Population'):
        internal.update(population=insee.get('InseeXls_Population'))

    if wiki.get('density'):
        internal.update(density=wiki.get('density'))

    if wiki.get('area'):
        internal.update(area=wiki.get('area'))

    if wiki.get('postal_codes'):
        internal.update(postal_codes=wiki.get('postal_codes'))

    internal_code = hash().make(
        hash().make(str([internal.get('name'), internal.get('type'), wiki.get('admin_hierarchy')])))
    internal.update(code=internal_code)

    source = {}
    if wiki_obj.get_document().get('code'):
        source.update(wiki=wiki_obj.get_document().get('code'))
    if gmap_obj.get_document().get('code'):
        source.update(gmap=gmap_obj.get_document().get('code'))
    if insee_obj and insee_obj.get_document().get('code'):
        source.update(insee=insee_obj.get_document().get('code'))

    internal.update(source=source)
    internal_obj = doc_factory.internal(internal.get('code'))
    internal_obj.update(internal)

i = 0
url_pull = ['https://fr.wikipedia.org/wiki/France']
for csv_file in files:
    with open(csv_file, encoding='utf-8') as admin_div_CSV:
        for line in csv.DictReader(admin_div_CSV, delimiter='\t'):
            try:
                i = i + 1
                print(i)
                dct = {}
                wiki_parsed = {}
                wiki = parser_wiki(line)

                insee = parser_insee(line)

                if wiki.get('url'):
                    if wiki.get('url') not in url_pull:
                        url_pull.append(wiki.get('url'))
                    print(wiki.get('url'))
                    wiki_obj = spider.get_wiki_url(url=wiki.get('url'))
                    wiki = wiki_obj.get_document()

                    try:
                        for name, value in wiki.get('admin_hierarchy', {}).items():
                            if value.get('url') in url_pull:
                                continue
                            else:
                                url_pull.append(value.get('url'))
                            print(value.get('url'))

                            wiki_admin = spider.get_wiki_url(url=value.get('url'))
                            wiki_admin_parsed= wiki_admin.get_document()

                            if wiki_admin_parsed.get('admin_hierarchy'):
                                gmap = gmap_by_address(wiki=wiki_admin_parsed)
                            else:
                                gmap = {}

                            if gmap.get('code'):
                                gmap_obj = doc_factory.gmaps(gmap.get('code'))
                                gmap_obj.update(gmap)
                            else:
                                gmap_obj = doc_factory.gmaps('dummy')
                            make_internal({}, {}, wiki_admin_parsed, wiki_admin, gmap, gmap_obj)
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt
                    except:
                        print('Error')
                        print(value)
                else:
                    wiki_obj = doc_factory.wiki('dummy')

                if insee.get('code'):
                    insee_obj = doc_factory.insee(insee.get('code'))
                    insee_obj.update(insee)
                else:
                    insee_obj = doc_factory.insee('dummy')

                if wiki.get('admin_hierarchy'):
                    gmap = gmap_by_address(wiki=wiki)
                else:
                    gmap = {}

                if gmap.get('code'):
                    gmap_obj = doc_factory.gmaps(gmap.get('code'))
                    gmap_obj.update(gmap)
                else:
                    gmap_obj = doc_factory.gmaps('dummy')

                make_internal(insee, insee_obj, wiki, wiki_obj, gmap, gmap_obj)
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                print('Error')
                print(line)

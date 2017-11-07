from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.config.Yaml import Yaml as Config
from lib.hashlib.sha512 import sha512 as hash
from lib.parser.wiki.Italy import Italy as ParserItalyWiki
from lib.factory.Loader import Loader as LoaderFactory
import csv
from lib.parser.map.google.GMapFactory import GMapFactory as MapFactory
from lib.spider.Spider import Spider
import pandas as pd

country = 'Italy'
lst_address = []

region_index = 1
provincia_index = 3
comune_index = 5
localita_index = 9
altitude_index = 13
codloc_index = 8
loc2011_index = 7
procom_index = 6
codcom_index = 4
codpro_index = 2
codreg_index = 0

config = Config('./config/config.yml')
doc_factory = DocFactory(config.get('mongodb'))
language='it'

spider = Spider(
    loader_factory=LoaderFactory,
    gmap_parser=MapFactory.italy,
    wiki_parser=ParserItalyWiki,
    doc_factory=doc_factory,
    language=language,
    config=config,
    use_cache=True
)

def gmap_by_address(address):
    objects = spider.get_gmap_address(address)

    gmap = {}
    if objects:
        gmap = objects[0].get_document()
        gmap.update(language=spider.gmap_loader._language)

    return gmap

df = pd.read_csv('./data/italy/indicatori_2011_localita.csv', delimiter=";", skiprows=[1], encoding='ISO-8859-1')

def make_internal(istat, istat_obj, wiki, wiki_obj, gmap, gmap_obj):
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
        if gmap.get('language') == 'it':
            internal.get('i18n', {}).update(it=gmap.get('name'))
        elif gmap.get('language') == 'en':
            internal.get('i18n', {}).update(en=gmap.get('name'))

    if gmap.get('admin_hierarchy'):
        internal.update(admin_hierarchy=gmap.get('admin_hierarchy', {}))

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
    if istat_obj and istat_obj.get_document().get('code'):
        source.update(insee=istat_obj.get_document().get('code'))

    internal.update(source=source)
    internal_obj = doc_factory.internal(internal.get('code'))
    internal_obj.update(internal)

    return internal_obj

def map_istat(row):
    return {
        'region': row[region_index],
        'provincia': row[provincia_index],
        'comune': row[comune_index],
        'localita': row[localita_index],
        'altitude': row[altitude_index],
        'codloc': row[codloc_index],
        'loc2011': row[loc2011_index],
        'procom': row[procom_index],
        'codcom': row[codcom_index],
        'codpro': row[codpro_index],
        'codreg': row[codreg_index]
    }

for index, row in df.iterrows():
    print(index)
    try:
        new_address = 'Italia, '
        if row[region_index]:
            new_address += row[region_index]
            if new_address not in lst_address:
                lst_address.append(new_address)
                gmap = gmap_by_address(new_address)
                if gmap.get('code'):
                    gmap_obj = doc_factory.gmaps(gmap.get('code'))
                    gmap_obj.update(gmap)
                else:
                    gmap_obj = doc_factory.gmaps('dummy')
                istat_code = hash().make(str(['Italia', row[region_index]]))
                istat_obj = doc_factory.istat(istat_code)
                wiki_obj = doc_factory.wiki('dummy')
                internal_obj = make_internal(row, istat_obj, {}, wiki_obj, gmap, gmap_obj)

            new_address += ', '
            if row[provincia_index]:
                new_address += row[provincia_index]
                if new_address not in lst_address:
                    lst_address.append(new_address)
                    gmap = gmap_by_address(new_address)
                    if gmap.get('code'):
                        gmap_obj = doc_factory.gmaps(gmap.get('code'))
                        gmap_obj.update(gmap)
                    else:
                        gmap_obj = doc_factory.gmaps('dummy')
                    istat_code = hash().make(str(['Italia', row[region_index], row[provincia_index]]))
                    istat_obj = doc_factory.istat(istat_code)
                    wiki_obj = doc_factory.wiki('dummy')
                    internal_obj = make_internal(row, istat_obj, {}, wiki_obj, gmap, gmap_obj)
                new_address += ', '
                if row[comune_index]:
                    new_address += row[comune_index]
                    if new_address not in lst_address:
                        lst_address.append(new_address)
                        gmap = gmap_by_address(new_address)
                        if gmap.get('code'):
                            gmap_obj = doc_factory.gmaps(gmap.get('code'))
                            gmap_obj.update(gmap)
                        else:
                            gmap_obj = doc_factory.gmaps('dummy')
                        istat_code = hash().make(str(['Italia', row[region_index], row[provincia_index], row[comune_index]]))
                        istat_obj = doc_factory.istat(istat_code)
                        wiki_obj = doc_factory.wiki('dummy')
                        internal_obj = make_internal(row, istat_obj, {}, wiki_obj, gmap, gmap_obj)
                    new_address += ', '
                    if row[localita_index]:
                        new_address += row[localita_index]
                        if new_address not in lst_address:
                            lst_address.append(new_address)
                            gmap = gmap_by_address(new_address)
                            if gmap.get('code'):
                                gmap_obj = doc_factory.gmaps(gmap.get('code'))
                                gmap_obj.update(gmap)
                            else:
                                gmap_obj = doc_factory.gmaps('dummy')
                            istat_code = hash().make(
                                str(['Italia', row[region_index], row[provincia_index], row[comune_index], row[localita_index]]))
                            istat_obj = doc_factory.istat(istat_code)
                            istat_obj.update(map_istat(row))
                            wiki_obj = doc_factory.wiki('dummy')
                            internal_obj = make_internal(row, istat_obj, {}, wiki_obj, gmap, gmap_obj)
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        print('Error in index [{}]'.format(index))
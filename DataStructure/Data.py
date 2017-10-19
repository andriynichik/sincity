from DataStructure.DataWiki import parser_wiki
from DataStructure.DataGMap import parser_gmap
from DataStructure.DataInsee import parser_insee
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.config.Yaml import Yaml as Config
from lib.hashlib.sha512 import sha512 as hash
import csv

files = [
    'DataStructure/20_08_17_canton_google_3.csv',
    'DataStructure/arrondissements_25_08_17_cards.csv',
    'DataStructure/Departements_28_08_17_cards.csv',
    'DataStructure/communes_17_09_17.csv'
]

config = Config('./config/config.yml')

doc_factory = DocFactory(config.get('mongodb'))
i = 0
for csv_file in files:
    with open(csv_file, encoding='utf-8') as admin_div_CSV:
        for line in csv.DictReader(admin_div_CSV, delimiter='\t'):
            try:
                i = i + 1
                print(i)
                dct = {}

                wiki = parser_wiki(line)

                gmap = parser_gmap(line)

                insee = parser_insee(line)

                if wiki.get('url'):
                    wiki_obj = doc_factory.wiki(wiki.get('url'))
                    wiki_obj.update(wiki)

                if gmap.get('code'):
                    gmap_obj = doc_factory.gmaps(gmap.get('code'))
                    gmap_obj.update(gmap)

                if insee.get('code'):
                    insee_obj = doc_factory.insee(insee.get('code'))
                    insee_obj.update(insee)

                internal = {}

                if gmap.get('name'):
                    internal.update(name=gmap.get('name'))
                elif wiki.get('name'):
                    internal.update(name=wiki.get('name'))

                if wiki.get('type'):
                    internal.update(type=wiki.get('type'))
                elif len(wiki.get('admin_hierarchy', [])):
                    internal.update(type='ADMIN_LEVEL_{}'.format(len(wiki.get('admin_hierarchy', [])) + 1))
                elif gmap.get('type'):
                    internal.update(type=gmap.get('type'))

                internal.update(i18n=wiki.get('i18n', {}))

                if gmap.get('G_Name_en'):
                    internal.get('i18n', {}).update(en=gmap.get('G_Name_en'))
                if gmap.get('G_Name_ru'):
                    internal.get('i18n', {}).update(ru=gmap.get('G_Name_ru'))
                if gmap.get('G_Name_uk'):
                    internal.get('i18n', {}).update(uk=gmap.get('G_Name_uk'))

                if wiki.get('admin_hierarchy'):
                    for obj in wiki.get('admin_hierarchy'):
                        internal.update({obj.get('type'): obj.get('name')})

                if wiki.get('capital'):
                    internal.update(capital=wiki.get('capital'))

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

                internal_code = hash().make(hash().make([internal.get('name'), internal.get('type'), wiki.get('admin_hierarchy')]))
                internal.update(code=internal_code)

                source = {}
                if wiki.get('code'):
                    source.update(wiki=wiki.get('code'))
                if gmap.get('code'):
                    source.update(gmap=wiki.get('code'))
                if insee.get('code'):
                    source.update(insee=insee.get('code'))

                internal.update(source=source)
                internal_obj = doc_factory.internal(internal.get('code'))
                internal_obj.update(internal)
            except:
                print(line)

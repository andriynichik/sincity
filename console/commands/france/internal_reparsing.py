from DataStructure.DataWiki import parser_wiki
from DataStructure.DataGMap import parser_gmap
from DataStructure.DataInsee import parser_insee
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.config.Yaml import Yaml as Config
from lib.hashlib.sha512 import sha512 as hash
from lib.parser.wiki.France import France as ParserFranceWiki
from lib.factory.Loader import Loader as LoaderFactory
import csv


files = [
    'DataStructure/20_08_17_canton_google_3.csv',
    'DataStructure/arrondissements_25_08_17_cards.csv',
    'DataStructure/Departements_28_08_17_cards.csv',
    'DataStructure/communes_17_09_17.csv'
]

config = Config('./config/config.yml')

doc_factory = DocFactory(config.get('mongodb'))
import datetime
import sys
from lib.factory.Loader import Loader as LoaderFactory
from lib.parser.map.google.GMapFactory import GMapFactory as MapFactory
from lib.config.Yaml import Yaml as Config
from lib.logger.File import File as FileLog
from lib.factory.StorageLocation import StorageLocation as DocFactory
from argparse import ArgumentParser


arg_parser = ArgumentParser(description='Download data from gmaps by address')
arg_parser.add_argument('-f', help='turn on the force mode')
arg_parser.add_argument('-a', help='address')
opts = arg_parser.parse_args()

config = Config('./config/config.yml')

loader = LoaderFactory.loader_gmaps_with_cache(
    gmaps_config=config.get('googlemaps'),
    storage_config=config.get('mongodb')
)
document_factory = DocFactory(config.get('mongodb'))
log = FileLog('./log/gmaps_address_france_{date}.log'.format(date=datetime.datetime.now().strftime('%Y-%m-%d')))
log.add('Start', log.INFO)
log.add('Params: [{0}]'.format(repr(opts).encode('utf-8')), log.INFO)

use_address = bool(opts.a)
address = opts.a if use_address else ''
force_update = opts.f


def update_meta(request, document):
    actual_doc = document.get_document()
    added_requests = [(tuple(x) if isinstance(x, list) else x) for x in actual_doc.get('requests', ())]
    added_requests.append(request)
    actual_doc.update(requests=list(set(added_requests)))
    document.update(actual_doc)

try:
    if use_address:
        address_content = loader.by_address(address=address)
        objects = MapFactory.france(address_content)
        for object in objects:
            code = object.get_place_id()
            if object.get_place_id():
                doc = document_factory.gmaps(code)
                if doc.is_new() or force_update:
                    dic = object.as_dictionary()
                    if dic.get('type'):
                        doc.update(object.as_dictionary())
                update_meta(request=address, document=doc)
    else:
        log.add('Wrong command', log.ERROR)
        print('use parameters like -a as address string')
except:
    message = str(sys.exc_info())
    log.add('Unexpected error: [{0}]'.format(message), log.ERROR)
    raise

log.add('Finish', log.INFO)

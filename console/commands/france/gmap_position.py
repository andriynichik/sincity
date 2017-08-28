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
arg_parser.add_argument('--lat', help='latitude')
arg_parser.add_argument('--lng', help='longitude')
opts = arg_parser.parse_args()

config = Config('./config/config.yml')

loader = LoaderFactory.loader_gmaps_with_cache(
    gmaps_config=config.get('googlemaps'),
    storage_config=config.get('mongodb')
)
document_factory = DocFactory(config.get('mongodb'))
log = FileLog('./log/gmaps_position_france_{date}.log'.format(date=datetime.datetime.now().strftime('%Y-%m-%d')))
log.add('Start', log.INFO)
log.add('Params: [{0}]'.format(repr(opts).encode('utf-8')), log.INFO)

use_position = opts.lat and opts.lng
latitude = opts.lat if use_position else ''
longitude = opts.lng if use_position else ''
force_update = opts.f

def update_meta(request, document):
    actual_doc = document.get_document()
    added_requests = actual_doc.get('requests', []) + [request]
    actual_doc.update(requests=list(set(added_requests)))
    document.update(actual_doc)

try:
    if use_position:
        position_content = loader.by_position(lat=latitude, lng=longitude)
        objects = MapFactory.france(position_content)
        for object in objects:
            code = object.get_place_id()
            if object.get_place_id():
                doc = document_factory.gmaps(code)
                if doc.is_new() or force_update:
                    doc.update(object.as_dictionary())
                update_meta(request=(latitude, longitude), document=doc)
    else:
        log.add('Wrong command', log.ERROR)
        print('use parameters like --lat as latitude and --lng as longitude')
except:
    message = str(sys.exc_info())
    log.add('Unexpected error: [{0}]'.format(message), log.ERROR)
    raise

log.add('Finish', log.INFO)
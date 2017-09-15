import datetime
import sys
from lib.factory.Loader import Loader
from lib.parser.wiki.Italy import Italy as WikiIt
from lib.config.Yaml import Yaml as Config
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.logger.File import File as FileLog
from argparse import ArgumentParser


config = Config('./config/config.yml')

arg_parser = ArgumentParser(description='Download data from wiki by link or search request')
arg_parser.add_argument('-f', help='turn on the force mode')
arg_parser.add_argument('-l', help='custom link to page with result(s)')
opts = arg_parser.parse_args()

insee_index = 0
name_index = 1
population_index = 2
force_update = opts.f
headers = {'User-Agent': 'Mozilla/5.0'}
loader = Loader.loader_with_mongodb(config.get('mongodb'))
document_factory = DocFactory(config.get('mongodb'))
log = FileLog('./log/wiki_page_italy_{date}.log'.format(date=datetime.datetime.now().strftime('%Y-%m-%d')))
log.add('Start', log.INFO)
log.add('Params: [{0}]'.format(repr(opts).encode('utf-8')), log.INFO)

message_format = 'Parsing request:[{0}]'

use_link = bool(opts.l)
custom_link = opts.l if use_link else ''


def update_meta(url, request, document):
    actual_doc = document.get_document()
    actual_doc.update(url=url)
    added_requests = [tuple(x) for x in actual_doc.get('requests', ())]
    added_requests.append(request)
    actual_doc.update(requests=list(set(added_requests)))
    document.update(actual_doc)

try:
    if use_link:
        log.add(message_format.format(custom_link), log.INFO)
        content, code = loader.load(custom_link, headers=headers)
        parser = WikiIt(content)

        if parser.is_many_answers():
            urls = parser.get_answers_links()
            for url in urls:
                doc = document_factory.wiki(url)
                if doc.is_new() or force_update:
                    page, code = loader.load(url, headers=headers)
                    page_parser = WikiIt(page)
                    if page_parser.is_location_page():
                        doc.update(page_parser.as_dictionary())
                update_meta(url=url, request=custom_link, document=doc)
        elif parser.is_location_page():
            doc = document_factory.wiki(custom_link)
            if doc.is_new() or force_update:
                doc.update(parser.as_dictionary())
            update_meta(url=custom_link, request=custom_link, document=doc)

    else:
        log.add('Wrong command', log.ERROR)
        print('use parameters like -l link to wiki page')
except:
    message = str(sys.exc_info())
    log.add('Unexpected error: [{0}]'.format(message), log.ERROR)
    raise

log.add('Finish', log.INFO)
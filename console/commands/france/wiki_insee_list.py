import pandas as pd
import datetime
import sys
from lib.factory.Loader import Loader
from lib.parser.wiki.France import France as WikiFr
from lib.config.Yaml import Yaml as Config
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.logger.File import File as FileLog
from argparse import ArgumentParser


config = Config('./config/config.yml')

arg_parser = ArgumentParser(description='Download data from wiki by csv file')
arg_parser.add_argument('-f', help='turn on the force mode')
arg_parser.add_argument('-s', help='source with insee list')
arg_parser.add_argument('-i', help='insee index in file')
arg_parser.add_argument('-n', help='name index in file')

arg_parser.add_argument('-l', help='request template where {query} is value from insee and query template')

opts = arg_parser.parse_args()

insee_index = opts.i if opts.i is not None else 0
name_index = opts.n if opts.n is not None else 1
population_index = 2
force_update = opts.f
headers = {'User-Agent': 'Mozilla/5.0'}
loader = Loader.loader_with_mongodb(config.get('mongodb'))
document_factory = DocFactory(config.get('mongodb'))
log = FileLog('./log/wiki_france_insee_list_{date}.log'.format(date=datetime.datetime.now().strftime('%Y-%m-%d')))
log.add('Start', log.INFO)
log.add('Params: [{0}]'.format(repr(opts).encode('utf-8')), log.INFO)

query_format = opts.l if opts.l is not None else "insee+{insee}"
url_format = opts.l if opts.l is not None else "https://fr.wikipedia.org/w/index.php?search={query}&title=Sp%C3%A9cial:Recherche&profile=default&fulltext=1&searchengineselect=mediawiki&searchToken=ac9zaxa1lggzxpdhc5ukg06t6"

message_format = 'Parsing request:[{request}]'

use_insee_list = bool(opts.s)
file_name_insee_list = opts.s if use_insee_list else './WorkBaseFile/BaseCommuneInInseeFR'


def update_meta(url, request, document):
    actual_doc = document.get_document()
    actual_doc.update(url=url)
    added_requests = actual_doc.get('requests', []) + [request]
    actual_doc.update(requests=list(set(added_requests)))
    document.update(actual_doc)

try:
    if use_insee_list:
        df = pd.read_csv(file_name_insee_list, delimiter="\t")
        for index, row in df.iterrows():
            try:
                insee = row[insee_index]
                name = row[name_index]
                population = row[population_index].replace(' ', '')
                request = query_format.format(insee=str(insee))
                log.add(message_format.format(request=request), log.INFO)
                url = url_format.format(query=request)
                content, code = loader.load(url, headers=headers)
                parser = WikiFr(content)

                if parser.is_many_answers():
                    urls = parser.get_answers_links()
                    for answer_url in urls:
                        doc = document_factory.wiki(answer_url)
                        if doc.is_new() or force_update:
                            page, code = loader.load(answer_url, headers=headers)
                            page_parser = WikiFr(page)
                            if page_parser.is_location_page():
                                doc.update(page_parser.as_dictionary())
                        update_meta(url=answer_url, request=url, document=doc)
                elif parser.is_location_page():
                    doc = document_factory.wiki(url)
                    if doc.is_new() or force_update:
                        doc.update(parser.as_dictionary())
                    update_meta(url=url, request=url, document=doc)
            except:
                log.add('Have error with insee [{insee}]'.format(insee=insee), FileLog.WARNING)
    else:
        log.add('Wrong command', log.ERROR)
        print('use parameters like -l csv file for wiki query')
except:
    message = str(sys.exc_info())
    log.add('Unexpected error: [{0}]'.format(message), log.ERROR)
    raise

log.add('Finish', log.INFO)
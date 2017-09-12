import datetime
import sys
import csv
from lib.factory.Loader import Loader
from lib.parser.wiki.France import France as WikiFr
from lib.config.Yaml import Yaml as Config
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.logger.File import File as FileLog
from argparse import ArgumentParser


config = Config('./config/config.yml')

arg_parser = ArgumentParser(description='Download data from wiki by link or search request')
arg_parser.add_argument('-f', help='turn on the force mode')
arg_parser.add_argument('-q', help='query for search')
opts = arg_parser.parse_args()

insee_index = 0
name_index = 1
population_index = 2
force_update = opts.f
headers = {'User-Agent': 'Mozilla/5.0'}
loader = Loader.loader_with_mongodb(config.get('mongodb'))
document_factory = DocFactory(config.get('mongodb'))
log = FileLog('./log/wiki_request_france_{date}.log'.format(date=datetime.datetime.now().strftime('%Y-%m-%d')))
log.add('Start', log.INFO)
log.add('Params: [{0}]'.format(repr(opts).encode('utf-8')), log.INFO)

url_format = "https://fr.wikipedia.org/w/index.php?search={0}&title=Sp%C3%A9cial:Recherche&profile=default&fulltext=1&searchengineselect=mediawiki&searchToken=ac9zaxa1lggzxpdhc5ukg06t6"
message_format = 'Parsing request:[{0}]'

use_request = bool(opts.q)
custom_request = opts.q if use_request else ''


def update_meta(url, request, document):
    actual_doc = document.get_document()
    actual_doc.update(url=url)
    added_requests = [tuple(x) for x in actual_doc.get('requests', ())]
    added_requests.append(request)
    actual_doc.update(requests=list(set(added_requests)))
    document.update(actual_doc)

def check_error(custom_request):
    try:
        if use_request:
            url = url_format.format(custom_request)
            log.add(message_format.format(custom_request), log.INFO)
            content, code = loader.load(url, headers=headers)
            parser = WikiFr(content)

            if parser.is_many_answers():
                urls = parser.get_answers_links()
                for answer_url in urls:
                    # print(answer_url)
                    doc = document_factory.wiki(answer_url)
                    if doc.is_new() or force_update:
                        page, code = loader.load(answer_url, headers=headers)
                        page_parser = WikiFr(page)
                        print(page_parser.as_dictionary())
                        # if page_parser.is_location_page():
                        #     doc.update(page_parser.as_dictionary())
                    # update_meta(url=answer_url, request=url, document=doc)
            elif parser.is_location_page():
                # doc = document_factory.wiki(url)
                # if doc.is_new() or force_update:
                #     doc.update(parser.as_dictionary())
                # update_meta(url=url, request=url, document=doc)
                # print(parser.as_dictionary())
                pass
        else:
            # log.add('Wrong command', log.ERROR)
            print('use parameters like -q query string for search in wiki in url format')
    except:
        message = str(sys.exc_info())
        log.add('Unexpected error: [{0}]'.format(message), log.ERROR)
        raise
check_error(custom_request)
# with open('./log/log_error.csv', 'r') as csvfile:
#     error_list = csv.reader(csvfile)
#     successful_attempts = 0
#     for error in list(error_list):
#         insee_error = (error[0].split())[0]
#         check_error(insee_error)
#         successful_attempts += 1
#     print(successful_attempts)

log.add('Finish', log.INFO)
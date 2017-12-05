from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.config.Yaml import Yaml as Config
import re
subject = "replacing the leftmost non-overlapping"
re.sub('e','E',subject)

config = Config('./config/config.yml')

doc_factory = DocFactory(config.get('mongodb'))

gmap_docs = doc_factory.gmaps_collection()
wiki_docs = doc_factory.wiki_collection()

for gmap_doc in gmap_docs.find():
    print(gmap_doc.get('name'), "\n")
    if gmap_doc.get('name'):
        gmap_doc.update(true_name=gmap_doc.get('name'))
        gmap_docs.update_one({'code':gmap_doc.get('code')}, {'$set': gmap_doc})

for wiki_doc in wiki_docs.find():
    print(wiki_doc.get('name'), "\n")
    if wiki_doc.get('name'):
        true_name = wiki_doc.get('name')
        true_name = re.sub('\s+\([^\)]+\)$', '', true_name)
        wiki_doc.update(true_name=true_name)
        wiki_docs.update_one({'code': wiki_doc.get('code')}, {'$set': wiki_doc})

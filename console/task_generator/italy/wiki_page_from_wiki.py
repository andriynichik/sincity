from lib.job.storage.MongoDB import MongoDB as Storage
from lib.job.wiki.PageTask import PageTask
from lib.config.Yaml import Yaml as Config
from lib.factory.StorageLocation import StorageLocation as DocFactory
import pandas as pd
import urllib.parse

country = 'Italia'
lst_address = []

region_index = 1
provincia_index = 3
comune_index = 5
localita_index = 9


config = Config('./config/config.yml').get('mongodb')

job_list = Storage(PageTask.get_name(country), config)

factory = DocFactory(config)
wiki = factory.wiki_collection()

filter = {
    'name': {'$exists': True, '$not': {'$size': 0}},
    'admin_hierarchy': {'$elemMatch': {'name': country}}
}

objects = wiki.find(filter)
for obj in objects:
    try:
        url = obj['url']
        if url:
            job_list.add(url)
    except KeyError:
        continue
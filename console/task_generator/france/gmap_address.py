from lib.job.storage.MongoDB import MongoDB as Storage
from lib.job.map.google.AddressTask import AddressTask
from lib.config.Yaml import Yaml as Config
from lib.factory.StorageLocation import StorageLocation as DocFactory

country = 'France'
lst_address = []

config = Config('./config/config.yml').get('mongodb')

job_list = Storage(AddressTask.TYPE, config)

factory = DocFactory(config)
wiki = factory.wiki_collection()

filter = {
    'name': {'$exists': True, '$not': {'$size': 0}},
    'admin_hierarchy': {'$elemMatch': {'name': country}}
}

for search_result in wiki.find(filter):
    try:
        new_address = ''
        for admin in search_result['admin_hierarchy']:
            name_admin = admin['name']
            new_address += name_admin
            if new_address not in lst_address:
                lst_address.append(new_address)
                new_address += ', '
            else:
                new_address += ', '
                continue
    except KeyError:
        continue

for address in lst_address:
    # job_list.add(adress)
    print(address)


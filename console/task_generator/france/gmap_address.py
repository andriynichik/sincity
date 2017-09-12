from lib.job.storage.MongoDB import MongoDB as Storage
from lib.job.map.google.AddressTask import AddressTask
from lib.config.Yaml import Yaml as Config
from lib.factory.StorageLocation import StorageLocation as DocFactory

country = 'France'
lst_adress = []

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
        new_adress = ''
        for admin in search_result['admin_hierarchy']:
            name_admin = admin['name']
            new_adress += name_admin
            if new_adress not in lst_adress:
                lst_adress.append(new_adress)
                new_adress += ', '
            else:
                new_adress += ', '
                continue
    except KeyError:
        continue

for adress in lst_adress:
    # job_list.add(adress)
    print(adress)


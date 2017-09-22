from lib.job.storage.MongoDB import MongoDB as Storage
from lib.job.map.google.PositionTask import PositionTask
from lib.config.Yaml import Yaml as Config
from lib.factory.StorageLocation import StorageLocation as DocFactory

country = 'Italia'

config = Config('./config/config.yml').get('mongodb')

job_list = Storage(PositionTask.get_name(country), config)


factory = DocFactory(config)
wiki = factory.wiki_collection()

filter = {
    'name': {'$exists': True, '$not': {'$size': 0}},
    'admin_hierarchy': {'$elemMatch': {'name': country}}
}

objects = wiki.find(filter)
for obj in objects:
    try:
        position = obj['center']
        position_list = ([pos for pos in position.values() if isinstance(pos, float)])
        if len(position_list) == 2:
            job_list.add(position)
    except KeyError:
        continue


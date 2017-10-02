from lib.job.TaskListMongoDB import TaskListMongoDB
from lib.job.map.google.AddressTask import AddressTask
from lib.job.ExecutorWithLimit import ExecutorWithLimit
from lib.job.storage.MongoDB import MongoDB as Storage
from lib.config.Yaml import Yaml as Config
from lib.factory.Loader import Loader as LoaderFactory
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.parser.map.google.Italy import Italy
from lib.logger.MongoDB import MongoDB as Log
from lib.Counter.CounterMongoDB import CounterMongoDB
from pymongo import MongoClient

force = True

config = Config('./config/config.yml')

country = 'Italy'

options = {}

gmaps_config = config.get('googlemaps')
gmaps_config.update(language='it')

loader = LoaderFactory.loader_gmaps_with_cache(
    gmaps_config=gmaps_config,
    storage_config=config.get('mongodb')
)
options.update(loader=loader)

doc_factory = DocFactory(config.get('mongodb'))

mongo_config = config.get('mongodb')

connection = MongoClient(mongo_config['host'], mongo_config['port'])

counter = CounterMongoDB(counter_name='gmap', start=1, end=gmaps_config.get('geocoding').get('limit'), step=1, ttl=86400, connection=connection)

options.update(doc_factory=doc_factory)

options.update(force_update=force)

options.update(parser=Italy)

storage = Storage(job_name=AddressTask.get_name(country), storage_config=config.get('mongodb'))

log = Log(log_name=AddressTask.get_name(country), config=config.get('mongodb'))

task_list = TaskListMongoDB(task_type=AddressTask.get_name(country), options=options, storage=storage, log=log)

executor = ExecutorWithLimit(task_list, counter)

executor.run()
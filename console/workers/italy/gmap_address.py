from lib.job.TaskListMongoDB import TaskListMongoDB
from lib.job.map.google.AddressTask import AddressTask
from lib.job.Executor import Executor
from lib.job.storage.MongoDB import MongoDB as Storage
from lib.config.Yaml import Yaml as Config
from lib.factory.Loader import Loader as LoaderFactory
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.parser.map.google.Italy import Italy
from lib.logger.MongoDB import MongoDB as Log

force = False

config = Config('./config/config.yml')

country = 'Italia'

options = {}

loader = LoaderFactory.loader_gmaps_with_cache(
    gmaps_config=config.get('googlemaps'),
    storage_config=config.get('mongodb')
)
options.update(loader=loader)

doc_factory = DocFactory(config.get('mongodb'))
options.update(doc_factory=doc_factory)

options.update(force_update=force)

options.update(parser=Italy)

storage = Storage(job_name=AddressTask.get_name(country), storage_config=config.get('mongodb'))

log = Log(log_name=AddressTask.get_name(country), config=config.get('mongodb'))

task_list = TaskListMongoDB(task_type=AddressTask.get_name(country), options=options, storage=storage, log=log)

executor = Executor(task_list)

executor.run()
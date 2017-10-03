from lib.job.TaskListMongoDB import TaskListMongoDB
from lib.job.wiki.PageTask import PageTask
from lib.job.Executor import Executor
from lib.job.storage.MongoDB import MongoDB as Storage
from lib.config.Yaml import Yaml as Config
from lib.factory.Loader import Loader as LoaderFactory
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.parser.wiki.Italy import Italy
from lib.logger.MongoDB import MongoDB as Log
from time import sleep


force = True

config = Config('./config/config.yml')

country = 'Italia'

options = {}

loader = LoaderFactory.loader_with_mongodb(storage_config=config.get('mongodb'))
options.update(loader=loader)

doc_factory = DocFactory(config.get('mongodb'))
options.update(doc_factory=doc_factory)

options.update(force_update=force)

options.update(parser=Italy)
options.update(headers={'User-Agent': 'Mozilla/5.0'})
storage = Storage(job_name=PageTask.get_name(country), storage_config=config.get('mongodb'))

log = Log(log_name=PageTask.get_name(country), config=config.get('mongodb'))

task_list = TaskListMongoDB(task_type=PageTask.get_name(country), options=options, storage=storage, log=log)

executor = Executor(task_list)

while True:
    executor.run()
    sleep(10)
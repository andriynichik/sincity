from lib.job.TaskListMongoDB import TaskListMongoDB
from lib.job.Executor import Executor
from lib.job.storage.MongoDB import MongoDB as Storage
from lib.config.Yaml import Yaml as Config
from lib.factory.Loader import Loader as LoaderFactory
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.parser.wiki.Italy import Italy
from lib.logger.MongoDB import MongoDB as Log
from time import sleep
from lib.job.wiki.PageRecursiveTask import PageRecursiveTask


force = True

config = Config('./config/config.yml')

options = {}

loader = LoaderFactory.loader_with_mongodb(storage_config=config.get('mongodb'))
options.update(loader=loader)

doc_factory = DocFactory(config.get('mongodb'))
options.update(doc_factory=doc_factory)

options.update(force_update=force)

options.update(parser=Italy)
options.update(headers={'User-Agent': 'Mozilla/5.0'})
storage = Storage(job_name=PageRecursiveTask.TYPE, storage_config=config.get('mongodb'))

log = Log(log_name=PageRecursiveTask.TYPE, config=config.get('mongodb'))

task_list = TaskListMongoDB(task_type=PageRecursiveTask.TYPE, options=options, storage=storage, log=log)

executor = Executor(task_list)

while True:
    executor.run()
    sleep(10)
from lib.job.TaskListMongoDB import TaskListMongoDB
from lib.job.map.google.AddressTask import AddressTask
from lib.config.Yaml import Yaml as Config
from lib.factory.Loader import Loader as LoaderFactory
from lib.factory.StorageLocation import StorageLocation as DocFactory


config = Config('./config/config.yml')

loader = LoaderFactory.loader_gmaps_with_cache(
    gmaps_config=config.get('googlemaps'),
    storage_config=config.get('mongodb')
)

document_factory = DocFactory(config.get('mongodb'))
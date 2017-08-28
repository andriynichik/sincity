from lib.factory.Loader import Loader as LoaderFactory
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.config.Yaml import Yaml as Config
from lib.job.map.google.AddressTask import AddressTask
from lib.job.map.google.PositionTask import PositionTask
from lib.job.storage.MongoDB import MongoDB
from lib.parser.map.google.GMapFactory import GMapFactory as MapFactory


class GMapTask:

    ADDRESS_LIST_NAME = 'gmaps_address'
    POSITION_LIST_NAME = 'gmaps_position'

    def __init__(self, country):
        self._country = country

    def _get_common_data(self, list_name, force=False):
        config = Config('./config/config.yml')

        loader = LoaderFactory.loader_gmaps_with_cache(
            gmaps_config=config.get('googlemaps'),
            storage_config=config.get('mongodb')
        )
        document_factory = DocFactory(config.get('mongodb'))

        options = {
            'loader': loader,
            'doc_factory': document_factory,
            'parser': getattr(MapFactory, self._country),
            'force_update': force
        }

        storage = MongoDB('{}_{}'.format(list_name, self._country), config.get('mongodb'))

        return options, storage

    def address(self, address, force=False):

        options, storage = self._get_common_data(list_name=self.ADDRESS_LIST_NAME, force=force)
        options.update(address=address)

        return AddressTask(options=options, storage=storage)

    def position(self, lat, lng, force=False):
        options, storage = self._get_common_data(list_name=self.POSITION_LIST_NAME, force=force)
        options.update(lat=lat)
        options.update(lng=lng)

        return PositionTask(options=options, storage=storage)

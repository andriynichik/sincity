from lib.job.map.google.AddressTask import AddressTask
from lib.job.map.google.PositionTask import PositionTask
from lib.job.wiki.PageRecursiveTask import PageRecursiveTask
from lib.job.wiki.PageTask import PageTask
from lib.job.wiki.RequestTask import RequestTask


class TaskList:

    TYPE = 'job'

    def __init__(self, task_type, options, storage, log):
        self._task_type = task_type
        self._storage = storage
        self._options = options
        self._log = log

    def get_next(self):
        pass

    def get_task_class(self, task_type):
        if task_type == AddressTask.TYPE:
            obj = AddressTask(options=self._options, storage=self._storage, log=self._log)
        elif task_type == PositionTask.TYPE:
            obj = PositionTask(options=self._options, storage=self._storage, log=self._log)
        elif task_type == PageRecursiveTask.TYPE:
            obj = PageRecursiveTask(options=self._options, storage=self._storage, log=self._log)
        elif task_type == PageTask.TYPE:
            obj = PageTask(options=self._options, storage=self._storage, log=self._log)
        elif task_type == RequestTask.TYPE:
            obj = RequestTask(options=self._options, storage=self._storage, log=self._log)
        else:
            raise Exception('[{}] task do not exists'.format(task_type))

        return obj
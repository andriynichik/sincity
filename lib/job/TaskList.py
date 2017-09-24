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
        if AddressTask.TYPE in task_type:
            obj = AddressTask(options=self._options, storage=self._storage, log=self._log)
        elif PositionTask.TYPE in task_type:
            obj = PositionTask(options=self._options, storage=self._storage, log=self._log)
        elif PageRecursiveTask.TYPE in task_type:
            obj = PageRecursiveTask(options=self._options, storage=self._storage, log=self._log)
        elif PageTask.TYPE in task_type:
            obj = PageTask(options=self._options, storage=self._storage, log=self._log)
        elif RequestTask.TYPE in task_type:
            obj = RequestTask(options=self._options, storage=self._storage, log=self._log)
        else:
            raise Exception('[{}] task do not exists'.format(task_type))

        return obj
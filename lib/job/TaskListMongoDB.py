from lib.job.TaskList import TaskList


class TaskListMongoDB(TaskList):
    TASK_TYPES = {

    }

    def __init__(self, task_type, options, storage, log):
        super(TaskListMongoDB, self).__init__(task_type, options, storage, log)

    def get_next(self):
        task_data = self._storage.get_one_active()
        if task_data:
            self._storage.as_in_progress(task_data.get('_id'))
            self._options.update(request=task_data.request)
            self._options.update(id=task_data.get('_id'))
            return self.get_task_class(self._task_type)
        else:
            return None

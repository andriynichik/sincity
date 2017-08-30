class Executor:

    def __init__(self, task_list):
        self._task_list = task_list

    def run(self):
            task = self._task_list.get_next()
            while task:
                task.execute()
                task.mark_as_complete()
                task = self._task_list.get_next()

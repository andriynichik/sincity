from time import sleep


class ExecutorWithLimit:

    def __init__(self, task_list, counter):
        self._task_list = task_list
        self._counter = counter

    def run(self):
            task = self._task_list.get_next()
            while task:
                while self._counter.is_can():
                    task.execute()
                    task.mark_as_complete()
                    task = self._task_list.get_next()
                    self._counter.step()
                sleep(10)
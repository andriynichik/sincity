from lib.job.Task import Task


class MapTask(Task):

    TYPE = 'map_task'

    @staticmethod
    def get_name(name):
        return '{}_{}'.format(MapTask.TYPE, name)

    @staticmethod
    def update_meta(request, document):
        actual_doc = document.get_document()
        added_requests = [(tuple(x) if isinstance(x, list) else x) for x in actual_doc.get('requests', ())]
        added_requests.append(request)
        actual_doc.update(requests=list(set(added_requests)))
        document.update(actual_doc)

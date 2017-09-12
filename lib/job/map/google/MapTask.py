from lib.job.Task import Task


class MapTask(Task):

    @staticmethod
    def update_meta(request, document):
        actual_doc = document.get_document()
        added_requests = [tuple(x) for x in actual_doc.get('requests', ())]
        added_requests.append(request)
        actual_doc.update(requests=list(set(added_requests)))
        document.update(actual_doc)

from lib.job.Task import Task


class MapTask(Task):

    def update_meta(request, document):
        actual_doc = document.get_document()
        added_requests = actual_doc.get('requests', []) + [request]
        actual_doc.update(requests=list(set(added_requests)))
        document.update(actual_doc)
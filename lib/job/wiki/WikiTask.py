from lib.job.Task import Task

class WikiTask(Task):

    @staticmethod
    def update_meta(url, request, document):
        actual_doc = document.get_document()
        actual_doc.update(url=url)
        added_requests = actual_doc.get('requests', []) + [request]
        actual_doc.update(requests=list(set(added_requests)))
        document.update(actual_doc)
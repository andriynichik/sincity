from lib.job.Task import Task


class WikiTask(Task):

    def __init__(self, options, storage, log):
        super(WikiTask, self).__init__(options=options, storage=storage, log=log)
        self.loader = self._options.get('loader')
        self.parser = self._options.get('parser')
        self.headers = self._options.get('headers')
        self.document_factory = self._options.get('doc_factory')

    @staticmethod
    def update_meta(url, request, document):
        actual_doc = document.get_document()
        actual_doc.update(url=url)
        added_requests = [(tuple(x) if isinstance(x, list) else x) for x in actual_doc.get('requests', ())]
        added_requests.append(request)
        actual_doc.update(requests=list(set(added_requests)))
        document.update(actual_doc)
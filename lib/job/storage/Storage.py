class Storage:

    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_ACTIVE = 'active'
    STATUS_COMPLETE = 'done'

    TYPE_GMAP_POSITION = 'gmap_position'
    TYPE_GMAP_ADDRESS = 'gmap_address'

    TYPE_WIKI_PAGE = 'wiki_page'
    TYPE_WIKI_REQUEST = 'wiki_request'
    TYPE_WIKI_RECURSIVE = 'wiki_recursive'

    def __init__(self):
        pass

    def get_active(self):
        pass

    def get_in_progress(self):
        pass

    def get_complete(self):
        pass

    def complete(self, id):
        pass
class entry(object):
    def __init__(self, path, name, permission, url):
        self._path = path
        self._name = name
        self._permission = permission
        self._url = url

class shared_menu_cache(object):
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state

from caches import shared_menu_cache, entry

class menu(object):
    def __init__(self, path, name, extension='html', permission=None, url=None):
        item = entry(path, name, extension, permission, url)
        shared_menu_cache.addEntry(item)

class navbar(menu):
    def __init__(self, path, extension='html', permission=None, url=None):
        super(navbar, self).__init__(path, u'navbar', extension, permission, url)
    
class sidebar(menu):
    def __init__(self, path, extension='html', permission=None, url=None):
        super(sidebar, self).__init__(path, u'sidebar', extension, permission, url)

class sitemap(menu):
    def __init__(self, path, extension='html', permission=None, url=None):
        super(sidebar, self).__init__(path, u'sitemap', extension, permission, url)

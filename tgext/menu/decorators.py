class menu(object):
    def __init__(self, path, name, permission=None, url=None):
        pass

class navbar(menu):
    def __init__(self, path, permission=None, url=None):
        super(navbar, self).__init__(path, u'navbar', permission, url)
    
class sidebar(menu):
    def __init__(self, path, permission=None, url=None):
        super(sidebar, self).__init__(path, u'sidebar', permission, url)

class sitemap(menu):
    def __init__(self, path, permission=None, url=None):
        super(sidebar, self).__init__(path, u'sitemap', permission, url)

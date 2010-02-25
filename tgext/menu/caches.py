import sys

from copy import deepcopy
from inspect import isfunction

from pylons import config
from tg.controllers import TGController

rootcon = None

class entry(object):
    def __init__(self, path, name, extension, permission, url, extras={}):
        self._path = path
        self._mpath = [x.strip() for x in path.split('||')]
        self._name = name
        self._extension = extension
        self._permission = permission
        self._url = url
        self.func = None
        self.base = None
        self.extras = deepcopy(extras)
        
        if 'class' not in self.extras:
            self.extras['class'] = []
        
    def __str__(self):
        return '%s at %s' % (str(self._path), str(self._url))

class shared_menu_cache(object):
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        if not(hasattr(self, '_menuitems')):
            self._menuitems = {}
        if not(hasattr(self, 'needs_update')):
            self.needs_update = True

    def addEntry(self, menuitem):
        self.needs_update = True
        if menuitem._name not in self._menuitems:
            self._menuitems[menuitem._name] = {}
        self._menuitems[menuitem._name][menuitem._path] = menuitem
        
    def removeEntry(self, menuitem):
        if menuitem._name in self._menuitems:
            if menuitem._path in self._menuitems[menuitem._name]:
                del self._menuitems[menuitem._name][menuitem._path]
            
    def getEntry(self, menuname, path):
        if menuname in self._menuitems:
            if path in self._menuitems[menuname]:
                return self._menuitems[menuname][path]
            else:
                return None
        else:
            return None
        
        return None
    
    def removeMenu(self, menuname):
        if menuname in self._menuitems:
            del self._menuitems[menuname]
            
    def getMenu(self, menuname):
        if self.needs_update:
            self.updateUrls()
        return self._menuitems[menuname] if menuname in self._menuitems else dict()
    
    def updateUrls(self):
        global rootcon
        if not rootcon:
            pname = '%s.controllers.root' % (config['package'].__name__)
            __import__(pname)
            rootcon = sys.modules[pname].RootController
        for menuname in self._menuitems:
            for menuitem in self._menuitems[menuname]:
                mi = self._menuitems[menuname][menuitem]
                mi._url = find_url(rootcon, self._menuitems[menuname][menuitem])
                if mi._url and mi._extension:
                    mi._url = '%s.%s' % (mi._url, mi._extension)
        self.needs_update = False


def find_url(root, menuitem):
    if ':' in str(menuitem._url):
        return menuitem._url
    if not(menuitem.base):
        n = menuitem.func.__name__
        if n in root.__dict__:
            if root.__dict__[n] is menuitem.func:
                return '/%s' % (n)
        for i in root.__dict__:
            controller = root.__dict__[i]
            if hasattr(controller, '_dispatch'):
                v = find_url(controller.__class__, menuitem)
                if v is not None:
                    return '/%s%s' % (i, v)
    else:
        for i in root.__dict__:
            controller = root.__dict__[i]
            if controller is menuitem.base:
                return '/%s/%s' % (i, menuitem._url)
            if hasattr(controller, '_dispatch'):
                v = find_url(controller.__class__, menuitem)
                if v is not None:
                    return '/%s%s' %(i, v)
    return None

def register_callback(menuname, func):
    if menuname not in callbacks:
        callbacks[menuname] = []
    
    if func not in callbacks[menuname]:
        callbacks[menuname].append(func)

def register_callback_navbar(func):
    register_callback(u'navbar', func)

def register_callback_sidebar(func):
    register_callback(u'sidebar', func)
    
def register_callback_sitemap(func):
    register_callback(u'sitemap', func)
    
def deregister_callback(menuname, func):
    if menuname not in callbacks:
        return
    
    if func not in callbacks[menuname]:
        return
    
    callbacks[menuname].remove(func)

def deregister_callback_navbar(func):
    deregister_callback(u'navbar', func)

def deregister_callback_sidebar(func):
    deregister_callback(u'sidebar', func)
    
def deregister_callback_sitemap(func):
    deregister_callback(u'sitemap', func)
    

shared_cache = shared_menu_cache()
callbacks = {'navbar': [], 'sidebar': [], 'sitemap': []}
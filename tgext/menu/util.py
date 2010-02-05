from pylons import config
from tg import request

from repoze.what.predicates import NotAuthorizedError
from repoze.what.predicates import has_permission

import tgext.menu.functions

use_tw2 = False
jquery_bgiframe_js = None
jquery_dimensions_js = None
jquery_position_js = None
jquery_jdmenu_js = None
jquery_jdmenu_css = None
jquery_js = None
sortorder = {}

class OutputEntry(object):
    def __init__(self, name, href=None):
        self.children = []
        self.href = href
        self.name = name

    def appendPath(self, name, href):
        # name is a list of paths, i.e.: ['Foo Spot', 'Bar']
        if len(name) > 1:
            try:
                idx = self.children.index(name[0])
            except ValueError:
                child = OutputEntry(name[0])
                self.children.append(child)
                idx = len(self.children)-1
            self.children[idx].appendPath(name[1:], href)
        else:
            child = OutputEntry(name[0], href)
            self.children.append(child)
    
    def __eq__(self, othername):
        return self.name == othername

def init_resources():
    global use_tw2, jquery_bgiframe_js, jquery_dimensions_js, jquery_position_js, jquery_jdmenu_js, jquery_jdmenu_css, jquery_js
    global sortorder

    sortorder = config.get('tgext_menu', {}).get('sortorder', {})

    use_tw2 = config.get('use_toscawidgets2', False)
    if use_tw2:
        from tw2.core import JSLink, CSSLink
        from tw2.jquery import jquery_js
                
        jquery_bgiframe_js = JSLink(
            modname=__name__,
            filename='static/js/jquery.bgiframe.js',
            resources=[jquery_js])
        
        jquery_dimensions_js = JSLink(
            modname=__name__,
            filename='static/js/jquery.dimensions.js',
            resources=[jquery_js])
        
        jquery_position_js = JSLink(
            modname=__name__,
            filename='static/js/jquery.positionBy.js',
            resources=[jquery_js, jquery_bgiframe_js, jquery_dimensions_js])
        
        jquery_jdmenu_js = JSLink(
            modname=__name__,
            filename='static/js/jquery.jdMenu.js',
            resources=[jquery_js, jquery_bgiframe_js, jquery_dimensions_js, jquery_position_js]).req()
        
        jquery_jdmenu_css = CSSLink(modname=__name__, filename='static/css/jquery.jdMenu.css').req()
    else:
        from tw.api import JSLink, CSSLink
        from tw.jquery import jquery_js, jquery_bgiframe_js, jquery_dimensions_js
        
        jquery_position_js = JSLink(
            modname=__name__,
            filename='static/js/jquery.positionBy.js',
            javascript=[jquery_js, jquery_bgiframe_js, jquery_dimensions_js])
    
        jquery_jdmenu_js = JSLink(
            modname=__name__,
            filename='static/js/jquery.jdMenu.js',
            javascript=[jquery_js, jquery_bgiframe_js, jquery_dimensions_js, jquery_position_js])
    
        jquery_jdmenu_css = CSSLink(modname=__name__, filename='static/css/jquery.jdMenu.css')
        
    tgext.menu.functions.sortorder = sortorder
    tgext.menu.functions.jquery_bgiframe_js = jquery_bgiframe_js
    tgext.menu.functions.jquery_dimensions_js = jquery_dimensions_js
    tgext.menu.functions.jquery_jdmenu_css = jquery_jdmenu_css
    tgext.menu.functions.jquery_jdmenu_js = jquery_jdmenu_js
    tgext.menu.functions.jquery_js = jquery_js
    tgext.menu.functions.jquery_position_js = jquery_position_js
    tgext.menu.functions.use_tw2 = use_tw2

def sort_entry(ent1, ent2):
    global sortorder
    idx = 0
    while idx < len(ent1._mpath) and idx < len(ent2._mpath):
        val1 = sortorder.get(ent1._mpath[idx], 999999)
        val2 = sortorder.get(ent2._mpath[idx], 999999)
        if val1 != val2:
            return cmp(val1, val2)
        idx += 1
    return cmp(ent1._mpath, ent2._mpath)

def permission_met(permission):
    if permission is None:
        return True
    elif type(permission) is str:
        try:
            has_permission(permission).check_authorization(request.environ)
            return True
        except NotAuthorizedError:
            return False
    else:
        try:
            permission.check_authorization(request.environ)
            return True
        except:
            return False
    


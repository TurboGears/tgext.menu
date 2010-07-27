import sys
from copy import deepcopy

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

rootcon = None

class OutputEntry(object):
    """
    An internal class, used to represent a single entry's information that is
    necessary to render it.
    
    This class is used instead of the list method that was present in earlier
    revisions as this creates a tree structure from the list data. The result
    is something that is easy to display, easy to sort, and easy to work with
    at display time. Note that the list representation is left alone earlier
    as a way to make life easier during menu manipulation time. The two
    classes complement each other.
    """
    def __init__(self, name, href=None, extras={}, icon=None):
        self.children = []
        self.href = href
        self.name = name
        self.extras = deepcopy(extras)
        self.icon = icon
        
        if 'class' not in self.extras:
            self.extras['class'] = []

    def appendPath(self, name, href, extras={}, icon=None):
        # name is a list of paths, i.e.: ['Foo Spot', 'Bar']
        if len(name) > 1:
            try:
                idx = self.children.index(name[0])
            except ValueError:
                child = OutputEntry(name[0], extras=extras, icon=icon)
                self.children.append(child)
                idx = len(self.children)-1
            self.children[idx].appendPath(name[1:], href, extras, icon)
        else:
            child = OutputEntry(name[0], href, extras=extras, icon=icon)
            self.children.append(child)
    
    def __eq__(self, othername):
        return self.name == othername

def init_resources():
    """
    This method is reponsible for configuring the JSLink and CSSLink widgets
    as necessary. It automatically detects and uses ToscaWidgets 2 when
    available and possible. Outside of that, it uses ToscaWidgets 1.
    """
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
    """
    A simple comparison function. It uses the sort order specified in the
    application's configuration, compares the menu entries, and returns the
    correct value depending on the configuration.
    """
    global sortorder
    idx = 0
    while idx < len(ent1._mpath) and idx < len(ent2._mpath):
        val1 = sortorder.get(ent1._mpath[idx], ent1.sortorder)
        val2 = sortorder.get(ent2._mpath[idx], ent2.sortorder)
        if val1 != val2:
            return cmp(val1, val2)
        idx += 1
    return cmp(ent1._mpath, ent2._mpath)

def permission_met(menu):
    """
    This is one of the more complicated methods. It works recursively.
    
    When called, it is given the root of the controller hierarchy. It looks
    for the path to the menu entry, and checks everything that it can along
    the way: allow_only on all controllers, and the (optional) permission on
    the method itself (which must be given to the @menu decorator or
    menu_append, see the README for details why and a workaround).
    """
    global rootcon
    retval = True
    
    if not rootcon:
        pname = '%s.controllers.root' % (config['package'].__name__)
        __import__(pname)
        rootcon = sys.modules[pname].RootController

    # Check to see if specific menu permission has been set
    permission = menu._permission
    if type(permission) is str:
        try:
            has_permission(permission).check_authorization(request.environ)
            return True
        except NotAuthorizedError:
            return False
    elif permission is not None:
        try:
            permission.check_authorization(request.environ)
            return True
        except:
            return False
    else:
        # No specific menu permission has been set, walk the tree
        lpath = menu._url.split('/')[1:]
        currcon = rootcon
        for component in lpath:
            if hasattr(currcon, 'allow_only'):
                try:
                    getattr(currcon, 'allow_only').check_authorization(request.environ)
                except:
                    return False
            if hasattr(currcon, component):
                currcon = getattr(currcon, component)
            else:
                break
        
    return True


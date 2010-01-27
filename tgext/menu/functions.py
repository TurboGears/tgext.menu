from mako.template import Template

from pkg_resources import Requirement, resource_string
divmenu = Template(resource_string(Requirement.parse("tgext.menu"),"tgext/menu/templates/divmenu.mak"))

from pylons import config
from repoze.what.predicates import NotAuthorizedError
from repoze.what.predicates import has_permission
from tg import request
from tw.api import JSLink, CSSLink
from tw.jquery import jquery_js, jquery_bgiframe_js, jquery_dimensions_js

from caches import shared_cache

jquery_position_js = JSLink(
    modname=__name__,
    filename='static/jquery.positionBy.js',
    javascript=[jquery_js, jquery_bgiframe_js, jquery_dimensions_js])

jquery_jdmenu_js = JSLink(
    modname=__name__,
    filename='static/jquery.jdMenu.js',
    javascript=[jquery_js, jquery_bgiframe_js, jquery_dimensions_js, jquery_position_js])

jquery_jdmenu_css = CSSLink(modname=__name__, filename='static/jquery.jdMenu.css')

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
            
def url_from_menu():
    # @todo: make a function that will return the url for the given menu path
    raise NotImplementedError('url_from_menu: Not Yet Implemented')

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
    
def render_menu(menuname, vertical=False):
    global sortorder
    jquery_js.inject()
    jquery_bgiframe_js.inject()
    jquery_dimensions_js.inject()
    jquery_position_js.inject()
    jquery_jdmenu_js.inject()
    
    if config.get('tgext_menu', {}).get('inject_css', False):
        jquery_jdmenu_css.inject()
    
    menutree = OutputEntry(menuname)
    menu = shared_cache.getMenu(menuname)
    sortorder = config.get('tgext_menu', {}).get('sortorder', {})
    shortmenu = [menu[key] for key in filter(lambda x: permission_met(menu[x]._permission), menu.keys())]
    for menuitem in sorted(shortmenu, sort_entry):
        menutree.appendPath(menuitem._mpath, str(menuitem._url))
    return divmenu.render(menulist=menutree, name=menuname, vertical_menu=vertical)

def render_navbar(vertical=False):
    return render_menu(u'navbar', vertical)

def render_sidebar(vertical=False):
    return render_menu(u'sidebar', vertical)

def render_sitemap(vertical=False):
    raise NotImplementedError('render_sitemap: Not Yet Implemented')
    return render_menu(u'sitemap', vertical)

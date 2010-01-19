from mako.template import Template

from pkg_resources import Requirement, resource_string
divmenu = Template(resource_string(Requirement.parse("tgext.menu"),"tgext/menu/templates/divmenu.mak"))

from pylons import config
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
    list1 = [x.strip() for x in ent1.split('||')]
    list2 = [x.strip() for x in ent2.split('||')]
    idx = 0
    while idx < len(list1) and idx < len(list2):
        val1 = sortorder.get(list1[idx], 999999)
        val2 = sortorder.get(list2[idx], 999999)
        if val1 != val2:
            return cmp(val1, val2)
        idx += 1
    return cmp(ent1, ent2)

def render_menu(menuname, inject_css=False):
    global sortorder
    jquery_js.inject()
    jquery_bgiframe_js.inject()
    jquery_dimensions_js.inject()
    jquery_position_js.inject()
    jquery_jdmenu_js.inject()
    
    if inject_css:
        jquery_jdmenu_css.inject()
    
    menutree = OutputEntry(menuname)
    menu = shared_cache.getMenu(menuname)
    sortorder = config.get('tgext', {}).get('menu', {}).get('sortorder', {})
    for key in sorted(menu.keys(), sort_entry):
        mpath = [x.strip() for x in key.split('||')]
        menutree.appendPath(mpath, str(menu[key]._url))
    return divmenu.render(menulist=menutree, name=menuname)

def render_navbar(inject_css=False):
    return render_menu(u'navbar', inject_css)

def render_sidebar(inject_css=False):
    return render_menu(u'sidebar', inject_css)

def render_sitemap(inject_css=False):
    raise NotImplementedError('render_sitemap: Not Yet Implemented')
    return render_menu(u'sitemap', inject_css)

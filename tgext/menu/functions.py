from copy import deepcopy
from sys import _getframe

from mako.template import Template

from pkg_resources import Requirement, resource_string
divmenu = Template(resource_string(Requirement.parse("tgext.menu"),"tgext/menu/templates/divmenu.mak"))

from pylons import config

from tgext.menu.caches import shared_cache, entry, callbacks
from tgext.menu.util import init_resources, OutputEntry
from tgext.menu.util import sort_entry, permission_met

jquery_bgiframe_js = jquery_dimensions_js = jquery_jdmenu_js = jquery_js = jquery_position_js = jquery_jdmenu_css = sortorder = None
use_tw2 = False

##############################################################################
## Section: url_from_menu, get_entry, switch_template
##############################################################################
def url_from_menu(menuname, menupath):
    menu = shared_cache.getMenu(menuname)
    menupath = [x.strip() for x in menupath.split('||')]
    for item in menu:
        if menu[item]._mpath == menupath:
            return menu[item]._url
    return None

def get_entry(menuname, menupath):
    return shared_cache.getEntry(menuname, menupath)

def switch_template(instr):
    global divmenu
    divmenu = Template(instr)

##############################################################################
## Section: Functions to append menu entries onto a menu
##############################################################################
def menu_append(path, name, extension=None, permission=None, url=None, base=None, extras={}, sortorder=999999, right=False, icon=None):
    item = entry(path, name, extension, permission, url, extras, sortorder, right, icon)
    item.base = base
    shared_cache.addEntry(item)

def navbar_append(path, extension=None, permission=None, url=None, base=None, extras={}, sortorder=999999, right=False, icon=None):
    menu_append(path, u'navbar', extension, permission, url, base, extras, sortorder, right, icon)

def sidebar_append(path, extension=None, permission=None, url=None, base=None, extras={}, sortorder=999999, right=False, icon=None):
    menu_append(path, u'sidebar', extension, permission, url, base, extras, sortorder, right, icon)

##############################################################################
## Section: Functions to remove menu entries from a menu
##############################################################################
def menu_remove(path, name):
    item = entry(path, name, None, None, None)
    shared_cache.removeEntry(item)

def navbar_remove(path):
    menu_remove(path, u'navbar')

def sidebar_remove(path):
    menu_remove(path, u'sidebar')

##############################################################################
## Section: Do final prep work to render a menu, and then call Mako to do the
## actual rendering
##############################################################################
def render_menu(menuname, vertical=False, active=None):
    global jquery_bgiframe_js, jquery_dimensions_js, jquery_jdmenu_js, jquery_js, jquery_position_js, jquery_jdmenu_css, sortorder, use_tw2
    
    if jquery_jdmenu_js is None:
        init_resources()


    if use_tw2:
        if config.get('tgext_menu', {}).get('inject_js', True):
            jquery_jdmenu_js.prepare()
    
        if config.get('tgext_menu', {}).get('inject_css', False):
            jquery_jdmenu_css.prepare()
    else:
        if config.get('tgext_menu', {}).get('inject_js', True):
            jquery_js.inject()
            jquery_bgiframe_js.inject()
            jquery_dimensions_js.inject()
            jquery_position_js.inject()
            jquery_jdmenu_js.inject()
        
        if config.get('tgext_menu', {}).get('inject_css', False):
            jquery_jdmenu_css.inject()
        
    menutree = OutputEntry(menuname)
    menu = shared_cache.getMenu(menuname)
    shortmenu = [menu[key] for key in filter(lambda x: permission_met(menu[x]), menu.keys())]
    if menuname in callbacks:
        for callback in callbacks[menuname]:
            try:
                shortmenu.extend(callback(menuname))
            except:
                pass
    if active:
        splitpath = [x.strip() for x in active.split('||')]
    else:
        splitpath = None
    for menuitem in sorted(shortmenu, sort_entry):
        if menuitem._mpath == splitpath:
            extras = deepcopy(menuitem.extras)
            extras['class'].append('active')
        else:
            extras = menuitem.extras
        menutree.appendPath(menuitem._mpath, str(menuitem._url), extras, menuitem.icon)
    return divmenu.render_unicode(menulist=menutree, name=menuname, vertical_menu=vertical)

def render_navbar(vertical=False, active=None):
    return render_menu(u'navbar', vertical, active)

def render_sidebar(vertical=False, active=None):
    return render_menu(u'sidebar', vertical, active)


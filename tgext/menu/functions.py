from mako.template import Template

from pkg_resources import Requirement, resource_string
divmenu = Template(resource_string(Requirement.parse("tgext.menu"),"tgext/menu/templates/divmenu.mak"))

from pylons import config

from tgext.menu.caches import shared_cache

from tgext.menu.util import init_resources, OutputEntry
from tgext.menu.util import sort_entry, permission_met

jquery_bgiframe_js = jquery_dimensions_js = jquery_jdmenu_js = jquery_js = jquery_position_js = jquery_jdmenu_css = sortorder = None
use_tw2 = False

def url_from_menu():
    # @todo: make a function that will return the url for the given menu path
    raise NotImplementedError('url_from_menu: Not Yet Implemented')

def render_menu(menuname, vertical=False):
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

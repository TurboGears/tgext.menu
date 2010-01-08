from mako.template import Template

from pkg_resources import Requirement, resource_string
divmenu = Template(resource_string(Requirement.parse("tgext.menu"),"tgext/menu/templates/divmenu.mak"))

from caches import shared_cache

def url_from_menu():
    # @todo: make a function that will return the url for the given menu path
    raise NotImplementedError('url_from_menu: Not Yet Implemented')

def render_menu(menuname):
    ul = []
    menu = shared_cache.getMenu(menuname)
    for key in sorted(menu.keys()):
        ul.append((key, str(menu[key]._url)))
    return divmenu.render(menulist=ul, name=menuname)

def render_navbar():
    return render_menu(u'navbar')

def render_sidebar():
    return render_menu(u'sidebar')

def render_sitemap():
    raise NotImplementedError('render_sitemap: Not Yet Implemented')
    return render_menu(u'sitemap')

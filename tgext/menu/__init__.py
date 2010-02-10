from tg.configuration import Bunch
from pylons import config

from decorators import menu, navbar, sidebar, sitemap
from functions import render_menu, render_navbar, render_sidebar, render_sitemap
from functions import menu_append, navbar_append, sidebar_append, sitemap_append
from functions import menu_remove, navbar_remove, sidebar_remove, sitemap_remove
from functions import url_from_menu

__all__ = ["menu", "navbar", "sidebar", "sitemap",
           "menu_append", "navbar_append", "sidebar_append", "sitemap_append",
           "menu_remove", "navbar_remove", "sidebar_remove", "sitemap_remove",
           "url_from_menu"]

def menu_variable_provider():
    menu_vars = Bunch (
        url_from_menu = url_from_menu,
        render_menu = render_menu,
        render_navbar = render_navbar,
        render_sidebar = render_sidebar,
        render_sitemap = render_sitemap
    )
    
    try:
        from genshi import HTML
        menu_vars['HTML'] = HTML
    except ImportError:
        pass
    
    if app_variable_provider:
        menu_vars.update(app_variable_provider())

    return menu_vars

app_variable_provider = config.get('variable_provider', None)
config.update(Bunch(
    variable_provider = menu_variable_provider
    ))

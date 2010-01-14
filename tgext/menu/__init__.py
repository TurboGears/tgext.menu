from tg.configuration import Bunch
from pylons import config

from decorators import menu, navbar, sidebar, sitemap
from functions import render_menu, render_navbar, render_sidebar, render_sitemap, url_from_menu

__all__ = ["menu", "navbar", "sidebar", "sitemap", "url_from_menu"]

def menu_variable_provider():
    menu_vars = Bunch (
        url_from_menu = url_from_menu,
        render_menu = render_menu,
        render_navbar = render_navbar,
        render_sidebar = render_sidebar,
        render_sitemap = render_sitemap
    )
    
    if app_variable_provider:
        menu_vars.update(app_variable_provider())

    return menu_vars

app_variable_provider = config.get('variable_provider', None)
config.update(Bunch(
    variable_provider = menu_variable_provider
    ))

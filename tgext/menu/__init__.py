import sys

from tg.configuration import Bunch
from pylons import config

from caches import register_callback, register_callback_navbar, register_callback_sidebar
from caches import deregister_callback, deregister_callback_navbar, deregister_callback_sidebar
from caches import entry
from decorators import menu, navbar, sidebar
from functions import render_menu, render_navbar, render_sidebar
from functions import menu_append, navbar_append, sidebar_append
from functions import menu_remove, navbar_remove, sidebar_remove
from functions import url_from_menu

__all__ = ["menu", "navbar", "sidebar",
           "menu_append", "navbar_append", "sidebar_append",
           "menu_remove", "navbar_remove", "sidebar_remove",
           "render_menu", "render_navbar", "render_sidebar",
           "register_callback", "register_callback_navbar", "register_callback_sidebar",
           "deregister_callback", "deregister_callback_navbar", "deregister_callback_sidebar",
           "url_from_menu", "entry"]

def menu_variable_provider():
    menu_vars = Bunch (
        url_from_menu = url_from_menu,
        render_menu = render_menu,
        render_navbar = render_navbar,
        render_sidebar = render_sidebar,
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

"""
tgext.menu is a tool to allow the web developer to specify where a given
method should appear in the menu hierarchy without having to deal with
templates. For how to use this, please see the README file. As this is geared
towards developers, the README file is the complete reference.

Copyright 2010 Michael J. Pedersen <m.pedersen@icelus.org>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including witho ut limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the fol lowing conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import sys

from tg.util import Bunch
from pylons import config

from caches import register_callback, register_callback_navbar, register_callback_sidebar
from caches import deregister_callback, deregister_callback_navbar, deregister_callback_sidebar
from caches import entry
from decorators import menu, navbar, sidebar
from functions import render_menu, render_navbar, render_sidebar
from functions import menu_append, navbar_append, sidebar_append
from functions import menu_remove, navbar_remove, sidebar_remove
from functions import url_from_menu, get_entry, switch_template

__all__ = ["menu", "navbar", "sidebar",
           "menu_append", "navbar_append", "sidebar_append",
           "menu_remove", "navbar_remove", "sidebar_remove",
           "render_menu", "render_navbar", "render_sidebar",
           "register_callback", "register_callback_navbar", "register_callback_sidebar",
           "deregister_callback", "deregister_callback_navbar", "deregister_callback_sidebar",
           "url_from_menu", "get_entry", "switch_template", "entry"]

# The below code is a bit of magic to make the usage of tgext.menu easier on
# the developer. Basically, it grabs the current variable_provider from the
# config, puts the tgext.menu variable provider into the config, and then
# returns the results from its own plus the original variable provider.
#
# By doing this, the developer does not have to remember to update the
# variable provider to provide the functions that the README says should be
# available in all templates.
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

app_variable_provider = config.get('tgext_menu_sub_variable_provider', None)
config.update(Bunch(
    variable_provider = menu_variable_provider
    ))

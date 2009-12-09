from caches import shared_menu_cache

def render_menu(menuname):
    ul = []
    menu = shared_menu_cache.getMenu(menuname)
    for key in sorted(menu.keys()):
        ul.append((key, str(menu[key].url)))
    return ul

def render_navbar():
    return render_menu(u'navbar')

def render_sidebar():
    return render_menu(u'sidebar')

def render_sitemap():
    # TODO: Generate the XML for a sitemap
    return render_menu(u'sitemap')


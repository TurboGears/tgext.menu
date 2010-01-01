from caches import shared_cache

def url_from_menu():
    # @todo: make a function that will return the url for the given menu path
    raise NotImplementedError('url_from_menu: Not Yet Implemented')

def render_menu(menuname):
    ul = []
    menu = shared_cache.getMenu(menuname)
    for key in sorted(menu.keys()):
        ul.append((key, str(menu[key]._url)))
    return ul

def render_navbar():
    return render_menu(u'navbar')

def render_sidebar():
    return render_menu(u'sidebar')

def render_sitemap():
    # TODO: Generate the XML for a sitemap
    return render_menu(u'sitemap')

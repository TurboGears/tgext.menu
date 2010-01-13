from mako.template import Template

from pkg_resources import Requirement, resource_string
divmenu = Template(resource_string(Requirement.parse("tgext.menu"),"tgext/menu/templates/divmenu.mak"))

from caches import shared_cache

class OutputEntry(object):
    def __init__(self, name, href=None):
        self.children = []
        self.href = href
        self.name = name

    def appendPath(self, name, href):
        # name is a list of paths, i.e.: ['Foo Spot', 'Bar']
        if len(name) > 1:
            midx = len(self.children)
            idx = 0
            found = False
            while not found and idx < midx:
                found = self.children[idx].name == name[0]
                idx += 1
            if not found:
                child = OutputEntry(name[0])
                self.children.append(child)
                idx = len(self.children)-1
            else:
                idx -= 1
            self.children[idx].appendPath(name[1:], href)
        else:
            child = OutputEntry(name[0], href)
            self.children.append(child)
            
def url_from_menu():
    # @todo: make a function that will return the url for the given menu path
    raise NotImplementedError('url_from_menu: Not Yet Implemented')

def render_menu(menuname):
    menutree = OutputEntry(menuname)
    menu = shared_cache.getMenu(menuname)
    for key in sorted(menu.keys()):
        mpath = [x.strip() for x in key.split('||')]
        menutree.appendPath(mpath, str(menu[key]._url))
    a=divmenu.render(menulist=menutree, name=menuname)
    print a
    return a

def render_navbar():
    return render_menu(u'navbar')

def render_sidebar():
    return render_menu(u'sidebar')

def render_sitemap():
    raise NotImplementedError('render_sitemap: Not Yet Implemented')
    return render_menu(u'sitemap')

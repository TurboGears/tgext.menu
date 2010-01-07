from tg import config, expose
from tg.controllers import TGController
from tgext.menu.test.model import DBSession
import tgext.menu.test.model as model

from tgext.menu import navbar

class NestedController(TGController):
    @navbar('Sub || Sub 1 || Nested 1')
    @expose('genshi:tgext.menu.test.templates.index')
    def index(self, *p, **kw):
        return dict()

class SubTwo(TGController):
    @navbar('ExitApp')
    @expose('genshi:tgext.menu.test.templates.index')
    def bybye(self, *p, **kw):
        return dict()

class SubController(TGController):
    nested = NestedController()
    Sub2 = SubTwo()
    
    @navbar('Sub || Sub 1')
    @expose('genshi:tgext.menu.test.templates.index')
    def index(self, *p, **kw):
        return dict()

    @navbar('Foo Spot || Sub || Foo')
    @expose('genshi:tgext.menu.test.templates.index')
    def foo(self, *p, **kw):
        return dict()

    @navbar('Foo Spot || Sub || Bar')
    @expose('genshi:tgext.menu.test.templates.index')
    def bar(self, *p, **kw):
        return dict()

    @navbar('Foo Spot || Sub || Baz')
    @expose('genshi:tgext.menu.test.templates.index')
    def baz(self, *p, **kw):
        return dict()
    
    @navbar('Foo Spot')
    @expose('genshi:tgext.menu.test.templates.index')
    def spot(self, *p, **kw):
        return dict()    


class RootController(TGController):
    sub1 = SubController()
    
    @navbar('TestHome')
    @expose('genshi:tgext.menu.test.templates.index')
    def index(self, *p, **kw):
        return dict()

    @navbar('Foo Spot || Foo')
    @expose('genshi:tgext.menu.test.templates.index')
    def foo(self, *p, **kw):
        return dict()

    @navbar('Foo Spot || Bar')
    @expose('genshi:tgext.menu.test.templates.index')
    def bar(self, *p, **kw):
        return dict()

    @navbar('Foo Spot || Baz')
    @expose('genshi:tgext.menu.test.templates.index')
    def baz(self, *p, **kw):
        return dict()


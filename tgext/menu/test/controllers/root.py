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

class SubController(TGController):
    nested = NestedController()
    
    @navbar('Sub || Sub 1')
    @expose('genshi:tgext.menu.test.templates.index')
    def index(self, *p, **kw):
        return dict()

class RootController(TGController):
    sub1 = SubController()
    
    @navbar('TestHome')
    @expose('genshi:tgext.menu.test.templates.index')
    def index(self, *p, **kw):
        return dict()


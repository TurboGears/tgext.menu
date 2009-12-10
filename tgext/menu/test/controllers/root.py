from tg import config, expose
from tg.controllers import TGController
from tgext.menu.test.model import DBSession
import tgext.menu.test.model as model

class RootController(TGController):
    @expose('genshi:tgext.menu.test.templates.index')
    def index(self, *p, **kw):
        return dict()
    
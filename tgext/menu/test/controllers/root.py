from tg import config, expose, request
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

    @navbar('Admin App', permission='manage')
    @expose('genshi:tgext.menu.test.templates.index')
    def admin(self, *p, **kw):
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
    
    #### The following are required for auth stuff to work
    @expose('tgext.menu.test.templates.login')
    def login(self, came_from='/'):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from='/'):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect('/login', came_from=came_from, __logins=login_counter)
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from='/'):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)



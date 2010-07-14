import os, sys
import tgext.menu
from pylons import config
from tg.test_stack import TestConfig, app_from_config
from tg.util import Bunch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from tgext.menu.test.model import metadata, DBSession, User, Group, Permission
from tgext.menu.caches import shared_cache, callbacks
from tgext.menu.caches import register_callback, register_callback_navbar, register_callback_sidebar
from tgext.menu.caches import deregister_callback, deregister_callback_navbar, deregister_callback_sidebar
from tgext.menu.test.model import Dictionary
from tgext.menu import menu_variable_provider, url_from_menu, sidebar_append, sidebar_remove, menu_append, menu_remove
from tgext.menu.util import init_resources

        
root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, root)
test_db_path = 'sqlite:///:memory:'
paths=Bunch(
            root=root,
            controllers=os.path.join(root, 'controllers'),
            static_files=os.path.join(root, 'public'),
            templates=os.path.join(root, 'templates')
            )

base_config = TestConfig(folder = 'rendering',
                         values = {'use_sqlalchemy': True,
                                   'use_toscawidgets2': True,
                                   'full_stack': True,
                                   'model':tgext.menu.test.model,
                                   'session':tgext.menu.test.model.DBSession,
                                   'pylons.helpers': Bunch(),
                                   'use_legacy_renderer': False,
                                   'renderers':['json', 'genshi', 'mako'],
                                   'default_renderer':'genshi',
                                   'use_dotted_templatenames': True,
                                   'paths':paths,
                                   'package':tgext.menu.test,
                                   'sqlalchemy.url':test_db_path,
                                   'variable_provider':menu_variable_provider,
                                   'auth_backend': 'sqlalchemy',
                                   'sa_auth': {
                                       'cookie_secret': 'ChAnGeMe',
                                       'dbsession': tgext.menu.test.model.DBSession,
                                       'user_class': User,
                                       'group_class': Group,
                                       'permission_class': Permission,
                                       'post_login_url': '/post_login',
                                       'post_logout_url': '/post_logout',
                                       'form_plugin': None,
                                       },
                                   
                                   'beaker.session.secret': 'ChAnGeMe',
                                   'beaker.session.key': 'tgext.menu.test',
                                   'tgext_menu': {
                                        'inject_css': True,
                                        'sortorder': {
                                            'TestHome': -1,
                                            'ExitApp': 99999999,
                                            'Baz' : 50,
                                            'Sub' : 50
                                            }
                                       }
                                  }
                         )

def setup_records(session):
    session.add(Dictionary(word=u'the'))
    session.add(Dictionary(word=u'quick'))
    session.add(Dictionary(word=u'brown'))
    session.add(Dictionary(word=u'fox'))
    session.add(Dictionary(word=u'jumped'))
    session.add(Dictionary(word=u'over'))
    session.add(Dictionary(word=u'the'))
    session.add(Dictionary(word=u'lazy'))
    session.add(Dictionary(word=u'dog'))

    u = User()
    u.user_name = u'manager'
    u.display_name = u'Example manager'
    u.email_address = u'manager@somedomain.com'
    u.password = u'managepass'

    session.add(u)

    g = Group()
    g.group_name = u'managers'
    g.display_name = u'Managers Group'

    g.users.append(u)

    session.add(g)

    p = Permission()
    p.permission_name = u'manage'
    p.description = u'This permission give an administrative right to the bearer'
    p.groups.append(g)

    session.add(p)

    session.flush()

def setup():
    global metadata, DBSession
    engine = create_engine(test_db_path)
    metadata.bind = engine
    metadata.drop_all()
    metadata.create_all()
    DBSession = sessionmaker(bind=engine)()
    setup_records(DBSession)
    DBSession.commit()

rendered_menu = """
<div id="navbar_div">
    <ul id="navbar" class="jd_menu">
        <li class="active first"><a href="/index">TestHome</a></li>
        <li>Sub
          <ul class="navbar_level1">
            <li class="first"><a href="/sub1/nested/jsonify.json">Get Json</a></li>
            <li><a href="http://www.google.com/">Google</a></li>
            <li><a href="/sub1/index">Sub 1</a>
              <ul class="navbar_level2">
                <li class="first last"><a href="/sub1/nested/index">Nested 1</a></li>
              </ul>
              </li>
            <li class="last"><a href="/sub1/nested/yan">Yet Another</a></li>
          </ul>
          </li>
        <li><a href="/nowhere">Add Me</a></li>
        <li><a href="/sub1/spot">Foo Spot</a>
          <ul class="navbar_level1">
            <li class="first"><a href="/baz">Baz</a></li>
            <li>Sub
              <ul class="navbar_level2">
                <li class="first"><a href="/sub1/baz">Baz</a></li>
                <li><a href="/sub1/bar">Bar</a></li>
                <li class="last"><a href="/sub1/foo">Foo</a></li>
              </ul>
              </li>
            <li id="foo_2"><a href="/bar">Bar</a></li>
            <li class="last" id="foo_1"><a href="/foo">Foo</a></li>
          </ul>
          </li>
        <li style="font-color: black"><a href="/sub1/styleme">Style Me</a> Right now!</li>
        <li class="last"><a href="/sub1/Sub2/bybye">ExitApp</a></li>
    </ul>
</div>
"""

rendered_admin_menu = """
<div id="navbar_div">
    <ul id="navbar" class="jd_menu">
        <li class="active first"><a href="/index">TestHome</a></li>
        <li>Sub
          <ul class="navbar_level1">
            <li class="first"><a href="/sub1/nested/jsonify.json">Get Json</a></li>
            <li><a href="http://www.google.com/">Google</a></li>
            <li><a href="/sub1/index">Sub 1</a>
              <ul class="navbar_level2">
                <li class="first last"><a href="/sub1/nested/index">Nested 1</a></li>
              </ul>
              </li>
            <li class="last"><a href="/sub1/nested/yan">Yet Another</a></li>
          </ul>
          </li>
        <li><a href="/nowhere">Add Me</a></li>
        <li><a href="/sub1/admin">Admin App</a></li>
        <li><a href="/arena/index">Arena</a></li>
        <li><a href="/sub1/spot">Foo Spot</a>
          <ul class="navbar_level1">
            <li class="first"><a href="/baz">Baz</a></li>
            <li>Sub
              <ul class="navbar_level2">
                <li class="first"><a href="/sub1/baz">Baz</a></li>
                <li><a href="/sub1/bar">Bar</a></li>
                <li class="last"><a href="/sub1/foo">Foo</a></li>
              </ul>
              </li>
            <li id="foo_2"><a href="/bar">Bar</a></li>
            <li class="last" id="foo_1"><a href="/foo">Foo</a></li>
          </ul>
          </li>
        <li><a href="/logout">Logout</a></li>
        <li style="font-color: black"><a href="/sub1/styleme">Style Me</a> Right now!</li>
        <li class="last"><a href="/sub1/Sub2/bybye">ExitApp</a></li>
    </ul>
</div>
"""

rendered_sidebar="""
<div id="sidebar_div">
    <ul id="sidebar" class="jd_menu">
        <li class="first last"><a href="/index">TestHome on the side</a></li>
    </ul>
</div>
"""

rendered_sidebar_added="""
<div id="sidebar_div">
    <ul id="sidebar" class="jd_menu">
        <li class="first"><a href="/">Add Sidebar</a></li>
        <li class="last"><a href="/index">TestHome on the side</a></li>
    </ul>
</div>
"""

class TestMenuDecorator:
    def __init__(self, *args, **kargs):
        global DBSession
        setup()
        base_config['session'] = DBSession
        base_config['sa_auth']['dbsession'] = DBSession
        self.app = app_from_config(base_config)
            
    def test_index_sidebar(self):
        resp = self.app.get('/')
        assert rendered_sidebar in resp, resp
        
    def test_sidebar_tools(self):
        sidebar_append('Add Sidebar', url='/')
        resp = self.app.get('/')
        assert rendered_sidebar_added in resp, "Added not found:\n" + str(resp)
        sidebar_remove('Add Sidebar')
        resp = self.app.get('/')
        assert rendered_sidebar in resp, "Added was still found:\n" + str(resp)

    def test_index_not_logged_in(self):
        resp = self.app.get('/')
        assert rendered_menu in resp, resp
        
    def test_inject_js(self):
        resp = self.app.get('/')
        assert 'jquery.js' in resp, resp
        assert 'jquery.bgiframe.js' in resp, resp
        assert 'jquery.dimensions.js' in resp, resp
        assert 'jquery.positionBy.js' in resp, resp
        assert 'jquery.jdMenu.js' in resp, resp

    def test_inject_css_true(self):
        resp = self.app.get('/')
        assert 'jquery.jdMenu.css' in resp, resp

    def test_inject_css_false(self):
        oldval = base_config['tgext_menu']['inject_css']
        base_config['tgext_menu']['inject_css'] = False
        resp = self.app.get('/')
        assert 'jquery.jdMenu.css' not in resp, resp
        base_config['tgext_menu']['inject_css'] = oldval

    def test_index_loggedin(self):
        resp = self.app.get('/login')
        form = resp.form
        form['login'] = u'manager'
        form['password'] = u'managepass'
        post_login = form.submit(status=302)
        assert post_login.location.startswith('http://localhost/post_login')
        resp = self.app.get('/')
        assert rendered_admin_menu in resp,resp
        
    def test_tw1(self):
        oldval = base_config['use_toscawidgets2']
        config['use_toscawidgets2'] = False
        init_resources()
        resp = self.app.get('/')
        assert 'tw.jquery.base/static/javascript/jquery-1.4.2.js' in resp, resp
        assert 'jquery.jdMenu.js' in resp, resp
        config['use_toscawidgets2'] = oldval

    def test_tw2(self):
        oldval = base_config['use_toscawidgets2']
        config['use_toscawidgets2'] = True
        init_resources()
        resp = self.app.get('/')
        assert 'tw2.jquery/static/jquery/1.4.2/jquery.js' in resp, resp
        assert 'jquery.jdMenu.js' in resp, resp
        config['use_toscawidgets2'] = oldval

    def test_url_from_menu(self):
        url = url_from_menu('navbar', 'TestHome')
        assert url=='/index', 'Expected "/index" and got "%s" when looking up "TestHome"'
        url = url_from_menu('navbar', 'Non-Existant')
        assert url is None, 'Expected None and got "%s" when looking up "Non-Existant"'
        
    def test_get_entries(self):
        resp = self.app.get('/')
        assert shared_cache.getEntry('No Such Menu', 'No Such Path') is None
        assert shared_cache.getEntry('navbar', 'No Such Path') is None
        assert shared_cache.getEntry('navbar', 'TestHome') is not None
    
    def test_str_entry(self):
        resp = self.app.get('/')
        ret = shared_cache.getEntry('navbar', 'TestHome')
        expected = "TestHome at /index"
        assert str(ret) == expected, 'Expected "%s", and got "%s"' % (expected, ret)
    
    def test_make_remove_menu(self):
        menu_append('Bogosity', 'Bogus')
        assert len(shared_cache.getMenu('Bogus')) > 0, "Didn't find the menu 'Bogus'"
        shared_cache.removeMenu('Bogus')
        assert len(shared_cache.getMenu('Bogus')) == 0, "Found the menu 'Bogus'"
        
    def callmeback(self):
        return None
    
    def test_callbacks(self):
        register_callback('bogus', self.callmeback)
        assert len(callbacks['bogus']) > 0
        deregister_callback('bogus', self.callmeback)
        assert len(callbacks['bogus']) == 0
        
        register_callback_navbar(self.callmeback)
        assert len(callbacks['navbar']) > 0
        deregister_callback_navbar(self.callmeback)
        assert len(callbacks['navbar']) == 0

        register_callback_sidebar(self.callmeback)
        assert len(callbacks['sidebar']) > 0
        deregister_callback_sidebar(self.callmeback)
        assert len(callbacks['sidebar']) == 0

        
    
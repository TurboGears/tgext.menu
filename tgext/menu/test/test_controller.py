import os, sys
import tgext.menu
from tg.test_stack import TestConfig, app_from_config
from tg.util import Bunch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from tgext.menu.test.model import metadata, DBSession, User, Group, Permission
from tgext.menu.caches import shared_cache
from tgext.menu.test.model import Dictionary
from tgext.menu import menu_variable_provider

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
        <li><a href="/index">TestHome</a></li>
        <li>Sub
          <ul class="navbar_level1">
            <li><a href="/sub1/index">Sub 1</a>
              <ul class="navbar_level2">
                <li><a href="/sub1/nested/index">Nested 1</a></li>
              </ul>
              </li>
          </ul>
          </li>
        <li><a href="/sub1/spot">Foo Spot</a>
          <ul class="navbar_level1">
            <li><a href="/baz">Baz</a></li>
            <li>Sub
              <ul class="navbar_level2">
                <li><a href="/sub1/baz">Baz</a></li>
                <li><a href="/sub1/bar">Bar</a></li>
                <li><a href="/sub1/foo">Foo</a></li>
              </ul>
              </li>
            <li><a href="/bar">Bar</a></li>
            <li><a href="/foo">Foo</a></li>
          </ul>
          </li>
        <li><a href="/sub1/Sub2/bybye">ExitApp</a></li>
    </ul>
</div>
"""

rendered_admin_menu = """
<div id="navbar_div">
    <ul id="navbar" class="jd_menu">
        <li><a href="/index">TestHome</a></li>
        <li>Sub
          <ul class="navbar_level1">
            <li><a href="/sub1/index">Sub 1</a>
              <ul class="navbar_level2">
                <li><a href="/sub1/nested/index">Nested 1</a></li>
              </ul>
              </li>
          </ul>
          </li>
        <li><a href="/sub1/admin">Admin App</a></li>
        <li><a href="/sub1/spot">Foo Spot</a>
          <ul class="navbar_level1">
            <li><a href="/baz">Baz</a></li>
            <li>Sub
              <ul class="navbar_level2">
                <li><a href="/sub1/baz">Baz</a></li>
                <li><a href="/sub1/bar">Bar</a></li>
                <li><a href="/sub1/foo">Foo</a></li>
              </ul>
              </li>
            <li><a href="/bar">Bar</a></li>
            <li><a href="/foo">Foo</a></li>
          </ul>
          </li>
        <li><a href="/logout">Logout</a></li>
        <li><a href="/sub1/Sub2/bybye">ExitApp</a></li>
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

    def test_index(self):
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


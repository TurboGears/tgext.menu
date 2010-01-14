import os, sys
import tgext.menu
from tg.test_stack import TestConfig, app_from_config
from tg.util import Bunch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from tgext.menu.test.model import metadata, DBSession
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
                                   'model':tgext.menu.test.model,
                                   'session':tgext.menu.test.model.DBSession,
                                   'pylons.helpers': Bunch(),
                                   'use_legacy_renderer': False,
                                   'renderers':['json', 'genshi', 'mako'],
                                   'default_renderer':'genshi',
                                   # this is specific to mako
                                   # to make sure inheritance works
                                   'use_dotted_templatenames': True,
                                   'paths':paths,
                                   'package':tgext.menu.test,
                                   'sqlalchemy.url':test_db_path,
                                   'variable_provider':menu_variable_provider
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
    session.flush()

def setup():
    engine = create_engine(test_db_path)
    metadata.bind = engine
    metadata.drop_all()
    metadata.create_all()
    session = sessionmaker(bind=engine)()
    setup_records(session)
    session.commit()

rendered_menu = """
<div id="navbar_div">
    <ul id="navbar" class="jd_menu">
        <li><a href="/sub1/Sub2/bybye">ExitApp</a></li>
        <li><a href="/sub1/spot">Foo Spot</a>
          <ul class="navbar_level1">
            <li><a href="/bar">Bar</a></li>
            <li><a href="/baz">Baz</a></li>
            <li><a href="/foo">Foo</a></li>
            <li>Sub
              <ul class="navbar_level2">
                <li><a href="/sub1/bar">Bar</a></li>
                <li><a href="/sub1/baz">Baz</a></li>
                <li><a href="/sub1/foo">Foo</a></li>
              </ul>
              </li>
          </ul>
          </li>
        <li>Sub
          <ul class="navbar_level1">
            <li><a href="/sub1/index">Sub 1</a>
              <ul class="navbar_level2">
                <li><a href="/sub1/nested/index">Nested 1</a></li>
              </ul>
              </li>
          </ul>
          </li>
        <li><a href="/index">TestHome</a></li>
    </ul>
</div>
"""
class TestMenuDecorator:
    def __init__(self, *args, **kargs):
        self.app = app_from_config(base_config)

    def test_index(self):
        resp = self.app.get('/')
        assert rendered_menu in resp, resp

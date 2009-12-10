import os, sys
import tgext.menu
from tg.test_stack import TestConfig, app_from_config
from tgext.menu.test.model import Dictionary
from tg.util import Bunch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from tgext.menu.test.model import metadata, DBSession

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
                                   'sqlalchemy.url':test_db_path
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

class TestMenuDecorator:
    def __init__(self, *args, **kargs):
        self.app = app_from_config(base_config)

    def test_index(self):
        resp = self.app.get('/')
        assert 'mainmenu' in resp, resp

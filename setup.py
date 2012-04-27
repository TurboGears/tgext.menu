# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import os

setup(
    name='tgext.menu',
    version='1.0rc3',
    description='Automatic menu/navbar/sidebar generation extension for TurboGears',
    author='Michael Pedersen',
    author_email='m.pedersen@icelus.org',
    url='http://bitbucket.org/pedersen/tgext.menu',
    install_requires=[
        "TurboGears2 >= 2.1",
        'Mako >= 0.2.4',
        ],
    keywords="turbogears2.widgets",
    setup_requires=["PasteScript >= 1.7"],
    paster_plugins=['PasteScript', 'Pylons', 'TurboGears2', 'tg.devtools'],
    packages=find_packages(exclude=['ez_setup', "*.test", "*.test.*", "test.*", "test"]),
    namespace_packages=['tgext'],
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['WebTest', 'BeautifulSoup', "zope.sqlalchemy >= 0.4 ", "tw2.jquery", "tw2.forms", "tw2.core"],
    message_extractors={'tgextmenu': [
            ('**.py', 'python', None),
            ('templates/**.mako', 'mako', None),
            ('templates/**.html', 'genshi', None),
            ('public/**', 'ignore', None)]},
    dependency_links=['http://www.turbogears.org/2.1/downloads/current/index'],
    zip_safe=False
)

# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='tgext.menu',
    version='0.1',
    description='',
    author='',
    author_email='',
    #url='',
    install_requires=[
        "TurboGears2 >= 2.1a3",
        "repoze.tm2 >= 1.0a4",
        'Mako >= 0.2.4',
        'tw.jquery'
        ],
    setup_requires=["PasteScript >= 1.7"],
    paster_plugins=['PasteScript', 'Pylons', 'TurboGears2', 'tg.devtools'],
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['tgext'],
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['WebTest', 'BeautifulSoup', "zope.sqlalchemy >= 0.4 ",],
    message_extractors={'tgextmenu': [
            ('**.py', 'python', None),
            ('templates/**.mako', 'mako', None),
            ('templates/**.html', 'genshi', None),
            ('public/**', 'ignore', None)]},
    package_data={'tgext.menu' : ['static/*', 'templates/*'] }
)

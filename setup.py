""" Setup file.
"""
import os
import re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
name = 'pyramid-request-log'

with open(os.path.join(here, 'README.md')) as r_file:
    README = r_file.read()
with open(os.path.join(here, 'CHANGES.rst')) as c_file:
    CHANGES = c_file.read()

with open(os.path.join(here, name.replace('-', '_'), '__init__.py')) as v_file:
    pattern = re.compile(r".*__version__ = '(.*?)'", re.S)
    version = pattern.match(v_file.read()).group(1)

requires = [
    'pyramid',
]

extras_require = {
    'test': [
        'nose',
        'coverage',
        'webtest',
        'pycodestyle',
        'testfixtures',
        'mock',
    ],
}

tests_requires = requires + extras_require['test']

setup(
    name=name,
    version=version,
    description='An Pyramid Plugin For loggin request',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='MoiTux',
    author_email='moitux@laposte.net',
    url='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='{}.tests'.format(name),
    install_requires=requires,
    extras_require=extras_require,
    tests_require=tests_requires,
)

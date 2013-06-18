#!/usr/bin/env python
from setuptools import setup, find_packages

try:
    README = open('README.rst').read()
except:
    README = None

# try:
#     LICENSE = open('LICENSE.txt').read()
# except:
#     LICENSE = None
#
LICENSE = ''

setup(
    name = 'django-tapatalk',
    version = '0.5.8.3',
    description='DjangoBB Tapatalk implementation',
    long_description=README,
    author = 'Sander van de Graaf',
    author_email = 'mail@svdgraaf.nl',
    license = LICENSE,
    url = 'http://github.com/svdgraaf/django-tapatalk/',
    packages = find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
    ],
)

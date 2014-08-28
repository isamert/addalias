#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

APPVERSION = '1.1'

setup(
    name='addalias',
    version=APPVERSION,
    author='İsa Mert Gürbüz',
    author_email='isamertgurbuz@gmail.com',
    description='A graphical and a commandline tool for adding/editing alias command.',
    url='https://github.com/isamert/addalias',
    license='MIT',
    scripts=['addalias'],
    data_files = [
      ('share/applications', ['data/addalias.desktop']),
      ('share/doc/addalias-%s' % APPVERSION, ['LICENSE', 'README.md']),
      ('share/pixmaps', ['data/addalias.png']),
    ],
    package_dir={'addalias': 'src'},
    packages=['addalias'],
)

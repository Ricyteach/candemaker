#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import re

from setuptools import find_packages
from setuptools import setup


def _read(file):
    with open(file, 'rb') as fp:
        return fp.read()
        
setup(
    name = 'candemaker',
    version = '0.0.1',
	url='https://github.com/Ricyteach/candemaker',
    author = 'Rick Teachey',
    author_email = 'rickteachey@cbceng.com',
    description = ('Tools for creating CANDE input files (.cid).'),
	license = 'BSD',
    keywords = 'cid msh CANDE fea',
	package_dir={'':'src'},
    packages=find_packages('src', exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    scripts=['scripts/test_script.bat'],
    install_requires=['parmatter'],
    include_package_data=True,
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', _read('README.rst').decode('utf-8')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', _read('CHANGELOG.rst').decode('utf-8'))
    ),
    classifiers=[
        'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: PyPy',
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
     ],
)
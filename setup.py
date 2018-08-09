#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os, fnmatch, re

version = ''
license = ''
with open('pyforms_terminal/__init__.py', 'r') as fd:
    content = fd.read()
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', content, re.MULTILINE).group(1)

    license = re.search(
        r'^__license__\s*=\s*[\'"]([^\'"]*)[\'"]', content, re.MULTILINE).group(1)

if not version: raise RuntimeError('Cannot find version information')
if not license: raise RuntimeError('Cannot find license information')

with open('README.md', 'r') as fd:
    long_description = fd.read()

setup(
    name='PyForms-Terminal',
    version=version,
    description="""Pyforms terminal is a software layer, part of the Pyforms main library. This layer implements the execution of a Pyforms application in the terminal.""",
    author='Ricardo Ribeiro',
    author_email='ricardojvr@gmail.com',
    license=license,
    url='https://github.com/UmSenhorQualquer/pyforms-terminal',
    
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    
    install_requires=[
        'requests',
        'idna',
        'simplejson',
        'opencv-python',
        'numpy',
        'confapp',
        'urllib3',
        'Pillow',
    ],
    packages=find_packages(),


    classifiers=[
        'Development Status :: 5 - Production/Stable',
        
        'Topic :: Software Development :: Build Tools',
        
        'Programming Language :: Python :: 3',

        'Environment :: Console',

        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',

        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        
    ],

    keywords='terminal development pyforms'
)

#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import re

version = ''
with open('pyforms_terminal/__init__.py', 'r') as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version: raise RuntimeError('Cannot find version information')

setup(
    name='PyForms-Terminal',
    version=version,
    description="""Pyforms is a Python 3 framework to develop terminal applications""",
    author='Ricardo Ribeiro',
    author_email='ricardojvr@gmail.com',
    license='MIT',
    url='https://github.com/UmSenhorQualquer/pyforms-terminal',
    install_requires=[
        'requests',
        'idna',
        'simplejson',
        'opencv-python',
        'confapp',
        'urllib3',
        'Pillow',
    ],
    packages=find_packages(),
)

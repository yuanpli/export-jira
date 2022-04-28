#!/usr/bin/env python
# encoding: utf-8
from setuptools import setup, find_packages
setup(
    name='Jira Python Project Setup File',
    version='0.1.0',
    packages=find_packages(exclude=('tests', 'docs'))
)

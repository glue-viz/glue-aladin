#!/usr/bin/env python

from __future__ import print_function

from setuptools import setup, find_packages

entry_points = """
[glue.plugins]
aladin=glue_aladin:setup
"""

with open('README.rst') as infile:
    LONG_DESCRIPTION = infile.read()

with open('glue_aladin/version.py') as infile:
    exec(infile.read())

setup(name='glue-aladin',
      version=__version__,
      description='My example plugin',
      long_description=LONG_DESCRIPTION,
      url="https://github.com/glue-viz/glue-plugin-template",
      author='',
      author_email='',
      packages=find_packages(),
      package_data={'glue_aladin':['*.ui']},
      entry_points=entry_points
    )

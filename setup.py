#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from os import path

"""
compranet-pipeline: Pipeline compranet
"""

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.Rmd')) as f:    
    long_description = f.read()

setup(
    name="compranet",
    version='0.0.1',
    description='Pipeline compranet',
    long_description=long_description,
    author_email='r.sanchezavalos@gmail.com',
    license='GPL v3',

    packages=find_packages(),

    test_suite='tests',

    install_requires=[
        'numpy',
        'pyyaml',
        'pandas',
        'scikit-learn',
        'sqlalchemy',
        'datetime',
        'scipy',
        'luigi',
        'Click',
        'python-dotenv'
    ],

    entry_points = {
        'console_scripts' : [
            'compranet = compranet.scripts.cli:main',
        ]
    },

    zip_safe=False
)


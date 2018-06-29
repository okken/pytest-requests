#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='pytest-requests',
    version='0.0.1',
    author='Brian Okken / Anthony Shaw',
    author_email='brian@pythontesting.net',
    maintainer='Brian Okken / Anthony Shaw',
    maintainer_email='brian@pythontesting.net',
    license='MIT',
    url='https://github.com/okken/pytest-requests',
    description='Fixtures to mock requests',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['pytest_requests'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=['pytest>=3.5.0', 'requests>=2.0.0,<3.0.0', 'mock>=2.0.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'requests = pytest_requests.plugin',
        ],
    },
)

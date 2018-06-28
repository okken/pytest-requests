# -*- coding: utf-8 -*-

from collections import namedtuple

import pytest
from .plugin import good, bad, patch


def pytest_addoption(parser):
    group = parser.getgroup('requests')
    group.addoption(
        '--foo',
        action='store',
        dest='dest_foo',
        default='2018',
        help='Set the value for the fixture "bar".'
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')


@pytest.fixture
def pytest_requests(request):
    namespace = namedtuple('Namespace', ['good', 'bad', 'patch'])
    return namespace(good, bad, patch)

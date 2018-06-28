# -*- coding: utf-8 -*-

from collections import namedtuple
import pytest
from .response import good, bad
from .patch import patch


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
def requests_mock(request):
    namespace = namedtuple('Namespace', ['good', 'bad', 'patch'])
    return namespace(good, bad, patch)

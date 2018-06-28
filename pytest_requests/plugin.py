# -*- coding: utf-8 -*-

from unittest.mock import patch as mock_patch
import contextlib
import requests
from .response import RequestsResponse
from .patch import RequestsPatch


@contextlib.contextmanager
def patch(uri):
    patch_obj = RequestsPatch(uri)
    patcher = mock_patch('requests.api.request', new=patch_obj)
    patched_request = patcher.start()
    patch_obj.patched_request = patched_request
    yield patch_obj
    patcher.stop()


def good(body, status_code=200, headers=None):
    """
    Return a "good" response, e.g. HTTP 200 OK
    with a given body.

    :param body: The body of the message
    :type  body: ``str``

    :param status_code: The HTTP status code
    :type  status_code: ``int``

    :param headers: Optional HTTP headers
    :type  headers: ``dict``

    >>> mock.returns = pytest_requests.good("hello")
    """
    if not isinstance(status_code, int):
        raise TypeError("Status Code must be of type `int`")
    return RequestsResponse(body, status_code)


def bad(body, status_code=500, headers=None):
    """
    Return a "bad" response, e.g. HTTP 500 Server-Error
    with a given body.

    :param body: The body of the message
    :type  body: ``str``

    :param status_code: The HTTP status code
    :type  status_code: ``int``

    :param headers: Optional HTTP headers
    :type  headers: ``dict``

    >>> mock.returns = pytest_requests.good("hello")
    """
    if not isinstance(status_code, int):
        raise TypeError("Status Code must be of type `int`")
    return RequestsResponse(body, status_code)

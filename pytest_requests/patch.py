# -*- coding: utf-8 -*-

from unittest.mock import patch as mock_patch
from requests.adapters import BaseAdapter
import contextlib
from .response import RequestsResponse

__all__ = ['patch']


@contextlib.contextmanager
def patch(uri):
    patch_obj = RequestsPatchedAdapter(uri)
    patcher = mock_patch('requests.adapters.HTTPAdapter', new=patch_obj)
    patched_request = patcher.start()
    patch_obj.patched_request = patched_request
    yield patch_obj
    patcher.stop()


class RequestsPatchedAdapter(BaseAdapter):
    """
    Context-Wrapper for the patched requests HTTP Adapter
    """

    def __init__(self, uri=None):
        """
        Instantiate a RequestsPatchedAdapter

        :param uri: The URI to patch
        :type  uri: ``str``
        """
        self.uri = uri
        self.response = None

    @property
    def returns(self):
        return self.response

    @returns.setter
    def returns(self, value):
        """
        Set the value that the patch returns

        :param value: The response to patch
        :type  value: :class:`pytest_requests.response.RequestsResponse`
        """
        if not isinstance(value, RequestsResponse):
            raise TypeError("Returns value must be an instance of `RequestsResponse`")
        self.response = value

    def send(self, request, stream=False, timeout=None, verify=True,
             cert=None, proxies=None):
        return self.response.to_response(request)
    
    def close(self):
        pass

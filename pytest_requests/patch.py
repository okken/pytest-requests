# -*- coding: utf-8 -*-

from mock import patch as mock_patch
from requests.adapters import BaseAdapter
from requests.compat import urlparse
import contextlib
from .response import RequestsResponse

__all__ = ["patch"]


@contextlib.contextmanager
def patch(uri):
    adapter = RequestsPatchedAdapter(uri)
    patched_adapter = mock_patch("requests.sessions.HTTPAdapter", new=adapter)
    patched_adapter.start()
    yield adapter
    patched_adapter.stop()


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
        self._response = None
        self._call_count = 0
        self._request = None

    def __call__(self):
        return self

    @property
    def returns(self):
        return self._response

    @returns.setter
    def returns(self, value):
        """
        Set the value that the patch returns

        :param value: The response to patch
        :type  value: :class:`pytest_requests.response.RequestsResponse`
        """
        if not isinstance(value, RequestsResponse):
            raise TypeError("Returns value must be an instance of `RequestsResponse`")
        self._response = value

    def send(
        self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None
    ):
        self._request = request
        self._call_count += 1
        url_parts = urlparse(request.url)
        if url_parts.path != self.uri:
            raise AssertionError(
                "URI path not matched, was {0} not {1}".format(url_parts.path, self.uri)
            )
        return self._response.to_response(request)

    def was_called_once(self):
        """
        Returns a ``bool`` for whether this URL has been called only once.

        :rtype: ``bool``
        """
        if self._call_count != 1:
            raise AssertionError(
                "URL was called {0} times, not 1".format(self._call_count)
            )
        else:
            return True

    def was_called_with_headers(self, headers):
        """
        Assert that URL was called with specific headers

        :rtype: ``bool``
        """
        for key, value in headers.items():
            assert key in self._request.headers
            assert value == self._request.headers[key]
        return True

    def close(self):
        pass

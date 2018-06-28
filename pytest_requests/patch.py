# -*- coding: utf-8 -*-

from .response import RequestsResponse


class RequestsPatch(object):
    """
    Context-Wrapper for the patched requests instance
    """

    def __init__(self, uri):
        """
        Instantiate a RequestsPatch

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

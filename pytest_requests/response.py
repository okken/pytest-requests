# -*- coding: utf-8 -*-

import sys
from requests import Response
from io import BytesIO
import json


# Instead of depending on six
if sys.version_info.major == 3:
    def ensure_bytes(string):
        if isinstance(string, bytes):
            return string
        else:
            return string.encode()
else:
    def ensure_bytes(string):
        if isinstance(string, unicode):
            return string.encode()
        else:
            return string


def good(body, status_code=200, headers={}):
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
    return RequestsResponse(body, status_code=status_code, headers=headers)


def bad(body, status_code=500, headers={}):
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
    return RequestsResponse(body, status_code=status_code, headers=headers)


class RequestsResponse(object):
    """
    Abstraction of :class:`requests.Response`
    """

    def __init__(self, body, status_code, headers={}):
        """
        Instantiate a :class:`RequestsResponse`

        :param body: The body of the response, or a dictionary for JSON data
        :type  body: ``str`` or ``dict``

        :param status_code: The HTTP status code
        :type  status_code: ``int``

        :param headers: Headers for the response
        :type  headers: ``dict``
        """
        if isinstance(body, dict):
            body = json.dumps(body)

        self.body = body
        self.status_code = status_code
        self.headers = headers

    def as_json(self):
        """
        Set the response as a application/json MIME type
        """
        self.headers["Content-Type"] = "application/json"
        return self

    def as_html(self):
        """
        Set the response as a text/html MIME type
        """
        self.headers["Content-Type"] = "text/html"
        return self

    def as_type(self, mime_type):
        """
        Set the Content-Type header of the response
        
        :param mime_type: The MIME type, e.g. text/html
        :type  mime_type: ``str``
        """
        self.headers["Content-Type"] = mime_type
        return self

    def to_response(self, request):
        """
        Convert the response to a native :class:`requests.Response`
        instance

        :param request: The request instance
        :type  request: :class:`requests.Request`

        :rtype: :class:`requests.Response`
        """
        response = Response()
        response.url = request.url
        response.raw = BytesIO(ensure_bytes(self.body))
        response.status_code = self.status_code
        response.headers = self.headers
        response.request = request
        response._content = ensure_bytes(self.body)
        return response

# -*- coding: utf-8 -*-

from requests import Response
from io import BytesIO


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


class RequestsResponse(object):
    """
    Abstraction of :class:`requests.Response`
    """

    def __init__(self, body, status_code, headers={}):
        """
        Instantiate a :class:`RequestsResponse`

        :param body: The body of the response
        :type  body: ``str``

        :param status_code: The HTTP status code
        :type  status_code: ``int``

        :param headers: Headers for the response
        :type  headers: ``dict``
        """
        self.body = body
        self.status_code = status_code
        self.headers = headers

    def as_json(self):
        """
        Set the response as a application/json MIME type
        """
        self.headers['Content-Type'] = 'application/json'

    def as_html(self):
        """
        Set the response as a text/html MIME type
        """
        self.headers['Content-Type'] = 'text/html'

    def as_type(self, mime_type):
        """
        Set the Content-Type header of the response
        
        :param mime_type: The MIME type, e.g. text/html
        :type  mime_type: ``str``
        """
        self.headers['Content-Type'] = mime_type
    
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
        response.raw = BytesIO(self.body)
        response.status_code = self.status_code
        response.headers = self.headers
        response.request = request
        response._content = body
        return response

import logging
from urlparse import urlparse
from HTTPHeaders import HTTPHeaders


class HTTPRequest(object):
    def __init__(self, request):
        self.http_version = request.http_version
        url = urlparse(request.url)
        self.url = url.geturl()
        self.hostname = url.hostname
        self.method = request.method
        self.body_size = request.body_size
        self.headers_size = request.headers_size
        self.headers = HTTPHeaders(request.headers).headers

import logging
from HTTPHeaders import HTTPHeaders


class HTTPResponse(object):
    def __init__(self, response):
        self.http_version = response.http_version
        self.status_text = response.status_text
        self.status = response.status
        self.body_size = response.body_size
        self.headers_size = response.headers_size
        self.headers = HTTPHeaders(response.headers).headers

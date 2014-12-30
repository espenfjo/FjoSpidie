import logging
from urlparse import urlparse

from HTTPCookies import HTTPCookies
from HTTPResponse import HTTPResponse
from HTTPRequest import HTTPRequest
from HTTPHeaders import HTTPHeaders
from HTTPContent import HTTPContent

class HTTPEntry:
    def __init__(self, entry, number, database):
        harRequest = entry.request
        harResponse = entry.response
        self.url = urlparse(harRequest.url).geturl()
        self.response = HTTPResponse(harResponse)
        self.request = HTTPRequest(harRequest)
        self.num = number
        if har_response.content:
            self.content = HTTPContent(har_response.content, database)

        if har_response.cookies:
            self.cookies = HTTPCookies(har_response.cookies).cookies

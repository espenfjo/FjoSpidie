import logging
from HTTPCookie import HTTPCookie
class HTTPCookies(object):
    def __init__(self, cookies):
        self.cookies = []
        for cookie in cookies:
            self.cookies.append(HTTPCookie(cookie))

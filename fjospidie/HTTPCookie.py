class HTTPCookie(object):
    def __init__(self, cookie):
        self.name = cookie.name
        self.value = cookie.value
        self.path = cookie.path
        self.domain = cookie.domain
        self.expires = cookie.expires
        self.http_only = cookie.http_only
        self.secure = cookie.secure
        self.comment = cookie.comment

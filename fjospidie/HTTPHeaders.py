from HTTPHeader import HTTPHeader
class HTTPHeaders(object):
    def __init__(self, headers):
        self.headers = []
        for header in headers:
            self.headers.append(HTTPHeader(header))

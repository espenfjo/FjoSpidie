import logging
from urlparse import urlparse
import dns.resolver
from Utils import geoip

from HTTPCookies import HTTPCookies
from HTTPResponse import HTTPResponse
from HTTPRequest import HTTPRequest
from HTTPHeaders import HTTPHeaders
from HTTPContent import HTTPContent

class HTTPEntry:
    def __init__(self, entry, number, database):
        self.ip = None

        logger = logging.getLogger(__name__)

        har_request = entry.request
        har_response = entry.response
        url_object = urlparse(har_request.url)
        domain = url_object.netloc
        if ":" in domain:
            domain = (domain.split(":"))[0]
        if entry.server_ip_address == '':
            try:
                logger.debug("Trying to resolve %s", domain)
                answers = dns.resolver.query(domain, 'A')
                self.ip = answers[0].address
            except dns.resolver.NXDOMAIN:
                logger.error("No such domain %s", domain)
            except dns.resolver.Timeout:
                logger.error("Timed out while resolving %s", domain)
            except dns.exception.DNSException:
                logger.error("Unhandled exception while resolving %s", domain)
        else:
            self.ip = entry.server_ip_address

        if self.ip:
            self.geoip = geoip(self.ip)

        self.url = url_object.geturl()

        self.response = HTTPResponse(har_response)
        self.request = HTTPRequest(har_request)
        self.num = number
        if har_response.content:
            self.content = HTTPContent(har_response.content, database)

        if har_response.cookies:
            self.cookies = HTTPCookies(har_response.cookies).cookies

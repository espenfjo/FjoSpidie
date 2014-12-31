import logging
import re
from netaddr import IPNetwork, IPAddress, AddrFormatError
from fjospidie.Utils import geoip

class SuricataAlert(object):
    """
    Class representing a fast alert from Suricata
    """

    def __init__(self, alert, httplog, config):
        self.__config = config
        regex = r"(\S+)  \[\*\*\] \[(\d+):(\d+):(\d+)\] (.*?) \[\*\*\] \[Classification: (.*?)\] \[Priority: (\d+)\] {\S+} (.*?):(\d+) -> (.*?):(\d+)"
        matcher = re.compile(regex)
        result = matcher.match(alert)
        self.logger = logging.getLogger(__name__)

        self.time = result.group(1)
        self.gid = result.group(2)
        self.sid = result.group(3)
        self.rule_revision = result.group(4)
        self.alarm_text = result.group(5)
        self.classification = result.group(6)
        self.priority = int(result.group(7))
        self.src = "{}:{}".format(result.group(8), result.group(9))
        self.dst = "{}:{}".format(result.group(10), result.group(11))
        self.src_geoip = geoip(result.group(8))
        self.dst_geoip = geoip(result.group(10))
        self.http_method = None
        self.http_request = None
        self.__check_http(httplog)

    def __check_turnaround(self, src):
        """Check if source of alert is us, if not is probably a http response"""
        self.logger.debug("Checking if {} is in {}".format(src, self.__config.mynet))
        try:
            return not IPAddress((src.split(':'))[0]) in IPNetwork(self.__config.mynet)
        except AddrFormatError as err:
            self.logger.error("Error decoding IP {}: {}".format(src, err))
            return False

    def __check_http(self, httplog):
        """
        Find the http request from Suricatas HTTP log to match with
        requests from the HAR log
        """
        for line in httplog:
            src_dst = (line.split("[**]"))[8]
            src = (src_dst.split(" "))[1].strip()
            dst = (src_dst.split(" "))[3].strip()
            if self.__check_turnaround(self.src):
                real_src = dst
                dst = src
                src = real_src

            if self.src == src and self.dst == dst:
                http_request = (line.split("[**]"))[1].lstrip()
                host = (line.split(" "))[1].strip()
                self.http_method = (line.split("[**]"))[4].strip()
                self.http_request = "^(http|https|ftp)://{}{}$".format(host, http_request.strip())
                return

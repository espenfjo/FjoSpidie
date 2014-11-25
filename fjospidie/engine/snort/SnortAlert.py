import re
from netaddr import IPNetwork, IPAddress
from datetime import datetime


class SnortAlert:

    def __init__(self, alert, httplog, config):
        self.__config = config
        text_parts = alert.split("[**]")
        self.alarm_text = (re.compile("\[\d+:\d+:\d+\]").split(text_parts[1]))[1].strip()
        space_parts = alert.split(" ")
        self.classification = ((text_parts[2].split("["))[1]).split("]")[0]
        pri = (re.compile("\s+").split((((text_parts[2].split("["))[2]).split("]")[0])))[1]
        self.priority = int(pri)
        self.time = space_parts[0]
        self.dst = (((text_parts[2].split("} "))[1]).split("->"))[0].strip()
        self.src = (((text_parts[2].split("} "))[1]).split("-> "))[1].strip()
        self.http_method = None
        self.http_request = None
        self.__check_http(httplog)

    def __check_turnaround(self, src):
        """Check if source of alert is us, if not is probably a http response"""
        return not IPAddress((src.split(':'))[0]) in IPNetwork(self.__config.mynet)

    def __check_http(self, httplog):
        for line in httplog:
            time = (line.split(" "))[0]
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

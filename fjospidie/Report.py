from argparse import Namespace
from bson.objectid import ObjectId
from datetime import datetime
import logging
from pymongo.son_manipulator import SONManipulator
import re
from types import NoneType
from uuid import uuid4

from HTTPEntries import HTTPEntries
from HTTPEntry import HTTPEntry
from HTTPHeader import HTTPHeader
from HTTPHeaders import HTTPHeaders
from HTTPRequest import HTTPRequest
from HTTPResponse import HTTPResponse
from HTTPContent import HTTPContent
from HTTPCookie import HTTPCookie
from engine.parser.YaraMatch import YaraMatch
from engine.suricata.SuricataAlert import SuricataAlert


class Report:
    def __init__(self, config, starttime):
        if not config.uuid:
            self.uuid = str(uuid4())
        else:
            self.uuid = config.uuid
        self.starttime = starttime
        self.entries = None
        self.graph = None
        self.endtime = None
        self.alerts = []

    def correlate_requests_and_alerts(self):
        for idx, alert in enumerate(self.alerts):
            if not alert.http_request:
                continue
            for entry in self.entries:
                request = entry.request
                logging.debug("Trying to match {} with {}".format(alert.http_request, request.url))
                m = re.match(alert.http_request, request.url)
                if m:
                    alert.request_id = entry.num
                    self.alerts[idx] = alert
                else:
                    continue

class Transform(SONManipulator):
    """
    Transform the Report object into Mongo eatable dicts
    """
    def transform_incoming(self, son, collection):
        """
        Convert a Report object into a MongoDB eatable dict
        """
        if isinstance(son, dict):
            for (key, value) in son.items():
                if isinstance(value, HTTPContent):
                    son[key] = self.transform_incoming(value.__dict__, collection)
                elif isinstance(value, HTTPResponse):
                    son[key] = self.transform_incoming(value.__dict__, collection)
                elif isinstance(value, HTTPRequest):
                    son[key] = self.transform_incoming(value.__dict__, collection)
                elif isinstance(value, HTTPCookie):
                    son[key] = self.transform_incoming(value.__dict__, collection)
                elif isinstance(value, dict):
                    son[key] = self.transform_incoming(value, collection)
                elif isinstance(value, list):
                    for (idx, item) in enumerate(value):
                        if isinstance(item, HTTPEntry):
                            son[key][idx] = self.transform_incoming(item.__dict__, collection)
                        elif isinstance(item, HTTPHeader):
                            son[key][idx] = self.transform_incoming(item.__dict__, collection)
                        elif isinstance(item, HTTPCookie):
                            son[key][idx] = self.transform_incoming(item.__dict__, collection)
                        elif isinstance(item, YaraMatch):
                            son[key][idx] = self.transform_incoming(item.__dict__, collection)
                        elif isinstance(item, SuricataAlert):
                            son[key][idx] = self.transform_incoming(item.__dict__, collection)
                        elif isinstance(item, dict):
                            son[key][idx] = self.transform_incoming(item, collection)
                        elif isinstance(item, list):
                            son[key][idx] = self.transform_incoming(item, collection)
                        elif isinstance(item, unicode):
                            pass
                        else:
                            logging.error("no inner match inner for {} type {}".format(item, type(item)))
                elif isinstance(value, Namespace):
                    son[key] = None
                elif isinstance(value, unicode):
                    pass
                elif isinstance(value, str):
                    pass
                elif isinstance(value, int):
                    pass
                elif isinstance(value, ObjectId):
                    pass
                elif isinstance(value, datetime):
                    pass
                elif isinstance(value, NoneType):
                    pass
                else:
                    logging.error("no match for {} type {}".format(value, type(value)))
        else:
            logging.error("No outer match for {} type {}".format(son, type(son)))
        return son

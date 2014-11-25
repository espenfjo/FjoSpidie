import yara
import logging
import fjospidie
import threading
import os
import base64
import re

from YaraMatches import YaraMatches

class YaraEngine(threading.Thread):

    def __init__(self, spidie):
        threading.Thread.__init__(self)
        logging.info("Initialising YaraEngine")

        self.pcap_path = None
        self.config = spidie.config
        self.yara_rules = self.config.yara_rules
        self.spidie = spidie
        self.init_rules()

    def init_rules(self):
        r = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.yara_rules)
        if not os.path.exists(r):
            logging.error("Default yara rule file {}: not found".format(r))
            return

        self.rules = yara.compile(r)

    def run(self):
        if not self.rules:
            logging.debug("Skipping YaraEngine scane since we have no rules")
            return

        logging.info("Starting YaraEngine")
        for idx, entry in enumerate(self.spidie.report.entries):
            if not entry.content:
                next
            grid_file = self.spidie.database.fs.get_version(md5=entry.content.md5)
            content = grid_file.read()
            matches = self.scan(content)
            entry.parser_match = YaraMatches(matches).matches
            print entry.parser_match
    def scan(self, rawdata):
        data = rawdata
        if self.isBase64(rawdata):
            try:
                data = base64.b64decode(rawdata)
            except:
                logging.info("Could not decode")
        return self.rules.match(data=data)

    def isBase64(self, s):
        return (len(s) % 4 == 0) and re.match('^[A-Za-z0-9+/]+[=]{0,2}$', s)

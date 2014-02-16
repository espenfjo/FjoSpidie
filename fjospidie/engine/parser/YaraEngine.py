import yara
import logging
import fjospidie
import threading
import os

class YaraEngine(threading.Thread):
    def __init__(self, config, report, entries):
        threading.Thread.__init__(self)
        logging.info("Initialising YaraEngine")

        self.pcap_path = None
        self.config = config
        self.yara_rules = self.config.yara_rules
        self.entries = entries
        self.report = report
        self.init_rules()

    def init_rules(self):
        r = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.yara_rules)
        if not os.path.exists(r):
            logging.error("Default yara rule file {}: not found".format(r))
            return

        self.rules = yara.compile(r)


    def run(self):
        if not self.rules:
            logging.debug("Skipping YaraEngine scane since we have no rules".format(cid))
            return

        logging.info("Starting YaraEngine")
        for entry in self.entries:
            harResponse = entry.response
            harContent = harResponse.content
            if not harContent:
                next

            self.scan(harContent.text, entry.contentid)

    def scan(self, data, cid):
        logging.debug("Scanning cid: {}".format(cid))
        matches = self.rules.match(data=data.encode('utf-8'))
        self.report.add_yara_matches(matches, cid)
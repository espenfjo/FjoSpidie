import logging
import threading
import json
import time
import os
from suricata.suricatasc import *
from suricata.SuricataAlert import SuricataAlert


class SuricataEngine(threading.Thread):

    def __init__(self, spidie, suricata_dir, pcap_path, socket):
        threading.Thread.__init__(self)
        self.socket = socket
        self.spidie = spidie
        self.suricata_dir = suricata_dir + "/suricata"
        self.pcap_path = pcap_path
        self.alerts = []
        self.logger = logging.getLogger(__name__)

    def run(self):
        self.logger.info("Starting SuricataEngine")
        os.makedirs(self.suricata_dir)
        debug = False
        if self.spidie.config.debug:
            debug = True

        sc = SuricataSC(self.socket, verbose=debug)
        try:
            sc.connect()
        except SuricataNetException, err:
            self.logger.error("Unable to connect to socket %s: %s", self.socket, err)
            return
        except SuricataReturnException, err:
            self.logger.error("Unable to negotiate version with server: %s", err)
            return

        arguments = {}
        arguments["filename"] = self.pcap_path
        arguments["output-dir"] = self.suricata_dir

        cmdret = sc.send_command("pcap-file", arguments)
        if cmdret["return"] == "NOK":
            self.logger.error(json.dumps(cmdret["message"], sort_keys=True, indent=4, separators=(',', ': ')))
        else:
            self.logger.debug(json.dumps(cmdret["message"], sort_keys=True, indent=4, separators=(',', ': ')))

        self.check_ok(sc, 0)

        alert_file = self.suricata_dir + "/fast.log"
        http_file = self.suricata_dir + "/http.log"
        with open(alert_file) as f:
            with open(http_file) as h:
                for line in f:
                    alert = SuricataAlert(line, h, self.spidie.config)
                    self.alerts.append(alert)
                    h.seek(0)

        self.spidie.report.alerts = self.alerts
        self.logger.info("Stopping SuricataEngine")

    def check_ok(self, sc, count):
        cmdret = sc.send_command("pcap-current")
        if cmdret["return"] == "NOK":
            self.logger.error(json.dumps(cmdret["message"], sort_keys=True, indent=4, separators=(',', ': ')))
        else:
            if cmdret["message"] == "None":
                self.logger.debug(json.dumps(cmdret["message"], sort_keys=True, indent=4, separators=(',', ': ')))
            else:
                if count < 60:
                    time.sleep(0.5)
                    count += 1
                    self.check_ok(sc, count)
                else:
                    self.logger.error("No result from suricata...")

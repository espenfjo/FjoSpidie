import threading
import logging
import subprocess
from snort.SnortAlert import SnortAlert
class SnortEngine(threading.Thread):
    def __init__(self, report, connections, snort_config, pcap_path):
        threading.Thread.__init__(self)
        self.connections = connections
        self.report = report
        self.snort_config = snort_config
        self.pcap_path = pcap_path
        self.alerts = []

    def run(self):
        logging.info("Starting SnortEngine")

        external_net = "["
        for connection in self.connections:
            external_net += connection + ','
        external_net += "]"

        snort_command = ["snort", "-c", self.snort_config, "-A", "console", "-q", "-N", "-r", self.pcap_path, "-S", "EXTERNAL_NET=" + external_net]
        logging.info("Running snort: " + " ".join(snort_command))
        snort = subprocess.Popen(snort_command, stdout=subprocess.PIPE)
        while True:
            line = snort.stdout.readline()
            if line != '':
                alert = SnortAlert(line)
                self.alerts.append(alert)
            else:
                break
        self.report.add_alerts( self.alerts)
        logging.info("Stopping SnortEngine")

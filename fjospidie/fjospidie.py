import random
import sys
import argparse
from configreader import parse_config
from browsermobproxy import Server
from datetime import datetime
from urlparse import urlparse
from Report import Report
from Node import Node
from Graph import Graph
from engine.PcapEngine import PcapEngine
import tempfile
from WebRunner import WebRunner
import psycopg2
import logging
nodes = []

class FjoSpidie:
    def __init__(self, config):
        self.config = config

        if self.config.verbose:
            logging.basicConfig(level=logging.INFO)
        if self.config.debug:
            logging.basicConfig(level=logging.DEBUG)

    def run(self):
        global nodes

        logging.info("Starting FjoSpidie 2.0")
        starttime  = datetime.now()
        ids_engine = None
        tempdir    = tempfile.mkdtemp(dir="/mnt/fjospidie")

        if self.config.suricata:
            from engine.SuricataEngine import SuricataEngine
        else:
            from engine.SnortEngine import SnortEngine

        report     = Report(starttime, self.config)
        proxy_port = random.randint(20000, 65534)
        start_url  = urlparse(self.config.url)
        nodes.append(Node(start_url.hostname))
        nodes[0].set_status(200)

        if not self.config.nopcap:
            pcap_engine = PcapEngine(report, tempdir)
            pcap_engine.start()

        webrunner = WebRunner(report)
        har = webrunner.run_webdriver(start_url, proxy_port, self.config, tempdir)

        if not self.config.nopcap:
            pcap_engine.stop()
            pcap_path = pcap_engine.pcap_path

        connections = webrunner.find_external_connections(har)
        entries     = har.entries
        report.insert_entries(entries)

        if not self.config.nopcap:
            if self.config.suricata:
                ids_engine   = SuricataEngine(self.config, report, connections, tempdir, pcap_path, "/mnt/fjospidie/socket")
            else:
                ids_engine   = SnortEngine(report, connections, self.config.snort_config, pcap_path)

            ids_engine.start()

        graph = Graph(entries, nodes, report)
        graph.create_graph()
        if not self.config.nopcap:
            ids_engine.join()
            if self.config.suricata:
                report.correlate_requests_and_alerts()

        report.insertp("UPDATE report set endtime=%s where id=%s", (datetime.now(), report.rid))
        report.db.commit()
        logging.info("Stopping FjoSpidie")

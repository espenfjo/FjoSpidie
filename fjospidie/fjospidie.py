from datetime import datetime
import importlib
import logging
from mongodb import MongoDB
import random
import tempfile
from urlparse import urlparse


from configreader import parse_config
from engine.PcapEngine import PcapEngine
from Graph import Graph
from HTTPEntries import HTTPEntries
from Node import Node
from Report import Report
from WebRunner import WebRunner
from Utils import ReportEnrichment

nodes = []
parsers = []


class FjoSpidie(object):
    def __init__(self, config):
        self.config = config
        self.database = None
        self.report = None
        self.logger = logging.getLogger(__name__)

    def run(self):
        global nodes
        self.logger.info("Starting FjoSpidie 2.1")
        starttime = datetime.now()
        ids_engine = None
        tempdir = tempfile.mkdtemp(dir="/mnt/fjospidie")

        if self.config.suricata:
            from engine.SuricataEngine import SuricataEngine

        self.database = MongoDB(self.config)
        self.report = Report(self.config, starttime)
        proxy_port = random.randint(20000, 65534)
        start_url = urlparse(self.config.url)
        reportEnricher = ReportEnrichment(self, start_url)
        reportEnricher.start()
        self.report.url = start_url.geturl()
        nodes.append(Node(start_url.hostname))
        nodes[0].set_status(200)

        if not self.config.nopcap:
            pcap_engine = PcapEngine(self, tempdir)
            pcap_engine.start()

        webrunner = WebRunner(self)
        har = webrunner.run_webdriver(start_url, proxy_port, self.config, tempdir)

        if not self.config.nopcap:
            pcap_engine.stop()
            pcap_path = pcap_engine.pcap_path

        self.report.connections = webrunner.find_external_connections(har)
        self.report.entries = HTTPEntries(har.entries, self.database).entries
        if self.config.parsers:
            for parser in self.config.parsers, :
                package = "fjospidie.engine.parser.{}".format(parser)
                try:
                    imported = importlib.import_module(package)
                    parser_class = getattr(imported, parser)
                    parser_engine = parser_class(self)
                    parsers.append(parser_engine)
                    parser_engine.start()
                except Exception, e:
                    self.logger.error("Error starting parser {}: {}".format(parser, e))
                    continue

        if not self.config.nopcap:
            ids_engine = SuricataEngine(self, tempdir,
                                        pcap_path, "/mnt/fjospidie/socket")
            ids_engine.start()

        graph = Graph(har.entries, nodes, self)
        graph.create_graph()
        if not self.config.nopcap:
            ids_engine.join()
            if self.config.suricata:
                self.report.correlate_requests_and_alerts()

        for parse_engine in parsers:
            parse_engine.join()

        reportEnricher.join()
        self.report.endtime = datetime.now()
        self.database.collection.insert(self.report.__dict__)
        self.logger.info("Stopping FjoSpidie")

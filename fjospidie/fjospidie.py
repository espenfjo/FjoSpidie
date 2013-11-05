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
from engine.SnortEngine import SnortEngine
#import engine
import WebRunner
import psycopg2
import logging
configfile = "fjospidie.conf"
nodes = []

def initialise():
    global nodes
    config = initialise_configuration()
    proxy_port = random.randint(20000, 65534)
    date = datetime.now()
    report = Report(date, config)
    start_url = urlparse(config.url)
    nodes.append(Node(start_url.hostname))
    nodes[0].set_status(200)
    pcap_engine = PcapEngine(report)
    pcap_engine.start()
    har = WebRunner.run_webdriver(start_url, proxy_port, config)
    pcap_engine.stop()
    pcap_path = pcap_engine.pcap_path
    
    connections = WebRunner.find_external_connections(har)
    entries = har.entries
    report.insert_entries(entries)

    snort_engine = SnortEngine(report, connections, config.snort_config, pcap_path)
    snort_engine.start()
    
    graph = Graph(entries, nodes, report)
    graph.create_graph()

    snort_engine.join()

    report.insertp("UPDATE report set endtime=%s where id=%s", (datetime.now(), report.rid))
    report.db.commit()

def initialise_configuration():
    """ Initialise configuration file and parse input arguments"""
    global configfile

    parser = argparse.ArgumentParser(
        description='Arguments to start FjoSpidie')

    parser.add_argument('--configfile', type=str, nargs=1,
                        help='FjoSpidie configuration file')
    args, remaining_argv = parser.parse_known_args()

    parser.add_argument('--url', type=str, required=True,
                        help='The URL to scan')
    parser.add_argument('--uuid', type=str,
                        help='Unique UUID of this report')
    parser.add_argument('--referer', type=str, nargs='?',
                        help='The HTTP_REFERER to use when loading the URL')
    parser.add_argument('--useragent', type=str, nargs=1,
                        help='The useragent used')
    parser.add_argument('--firefoxprofile', type=str, nargs=1,
                        help='The Firefox profile used to run Firefox')
    parser.add_argument('--snortconfig', type=str, nargs=1,
                        help='Snort configuration file')
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
    parser.add_argument("-d", "--debug", help="Debug output",
                    action="store_true")

    if args.configfile:
        configfile = args.configfile

    config = parse_config(configfile)
    parser.set_defaults(**config)
    args = parser.parse_args(remaining_argv)
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    return args

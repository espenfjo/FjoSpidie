from fjospidie.fjospidie import FjoSpidie
import argparse
from fjospidie.configreader import parse_config


def read_config():
    configfile = "fjospidie.conf"
    parser = argparse.ArgumentParser()
    description='Arguments to start FjoSpidie'

    parser.add_argument('--configfile', type=str, nargs=1,
                        help='FjoSpidie configuration file')
    args, remaining_argv = parser.parse_known_args()

    parser.add_argument('--url', type=str, required=True,
                        help='The URL to scan')
    parser.add_argument('--uuid', type=str,
                        help='Unique UUID of this report')
    parser.add_argument('--referer', type=str, nargs='?',
                        help='The HTTP_REFERER to use when loading the URL')
    parser.add_argument('--useragent', type=str, nargs='?',
                        help='The useragent used')
    parser.add_argument('--firefoxprofile', type=str, nargs=1,
                        help='The Firefox profile used to run Firefox')
    parser.add_argument('--snortconfig', type=str, nargs=1,
                        help='Snort configuration file')
    parser.add_argument('--nopcap', help='Doesnt fire up the pcap engine, and hence, doesnt fire up snort/suricata engines', action="store_true")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
    parser.add_argument("-d", "--debug", help="Debug output",
                    action="store_true")

    if args.configfile:
        configfile = args.configfile

    config = parse_config(configfile)
    parser.set_defaults(**config)
    args = parser.parse_args(remaining_argv)
    return args

config = read_config()
spidie = FjoSpidie(config)
spidie.run()

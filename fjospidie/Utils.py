"""
Various helper function used by several methods or classes
"""

import logging
import hashlib
import threading
import pygeoip
import dns.resolver
import os

def get_md5(data):
    """
    Get the MD5sum of the passed data
    """
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()

def geoip(ip):
    r = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../geoip")
    if not os.path.exists(r):
        logging.error("GeoIP not found at {}".format(r))
        return

    gorg = pygeoip.GeoIP('{}/GeoIPOrg.dat'.format(r))
    gcity = pygeoip.GeoIP('{}/GeoIPCity.dat'.format(r))
    gisp = pygeoip.GeoIP('{}/GeoIPISP.dat'.format(r))

    data = {}
    data = gcity.record_by_addr(ip)
    if data:
        data['organisation'] = gorg.org_by_addr(ip)
        data['isp'] = gisp.isp_by_addr(ip)
    else:
        print "WTF: {} is null!".format(ip)
    return data



class ReportEnrichment(threading.Thread):
    """
    Generate extra information about a report
    """
    def __init__(self, spidie, url):
        threading.Thread.__init__(self)
        self.spidie = spidie
        self.geoip_path = self.spidie.config.geoip
        self.url = url
        self.logger = logging.getLogger(__name__)


    def run(self):
        self.logger.info("Starting Report Enrichment engine")
        domain = self.url.netloc
        if ":" in domain:
            domain = (domain.split(":"))[0]
        answers = dns.resolver.query(domain, 'A')
        ip = answers[0].address
        self.spidie.report.ip = ip
        self.spidie.report.geoip = geoip(ip)
        self.logger.info("Stopping Report Enrichment engine")

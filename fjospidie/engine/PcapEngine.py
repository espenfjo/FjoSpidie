import logging
import tempfile
import fjospidie
import pcap
import subprocess
import threading
import ctypes
import inspect
import uuid
import psycopg2

class PcapEngine(threading.Thread):
    def __init__(self, report):
        threading.Thread.__init__(self)
        self.pcap_path = None
        self.report = report

    def run(self):
        logging.info("Starting PCAP engine")
        self.p = pcap.pcapObject()
        snaplen = 64 * 1024
        timeout = 1
        pcap_file = tempfile.NamedTemporaryFile(prefix="snort", suffix="pcap", delete=False)
        self.pcap_path = pcap_file.name
        logging.debug("PCAPing to " + self.pcap_path)
        dev = self.find_default_adapter()
        self.p.open_live(dev, snaplen, 0, timeout)
        dumper = self.p.dump_open(self.pcap_path)

        self.p.loop(-1,dumper)

    def find_default_adapter(self):
        route = subprocess.Popen(['/usr/bin/env', "netstat","-rn"], stdout=subprocess.PIPE)
        default = None
        while True:
            line = route.stdout.readline()
            if line != '':
                if line.startswith("default") or line.startswith("0.0.0.0"):
                    default = line
                    break
            else:
                break

        parts = default.split()
        if len(parts) >= 8:
            return parts[7]
        else:
            return parts[5]

    def stop(self):
        self.p.breakloop()
        self.add_to_db()

    def add_to_db(self):
        pcap = None
        with open(self.pcap_path, mode='rb') as file:
            pcap = file.read()
        logging.debug("Adding " + self.pcap_path + " to database")
        self.report.insertp("INSERT INTO pcap (report_id, data, uuid) VALUES (%s,%s, %s)",(self.report.rid,psycopg2.Binary(pcap), uuid.uuid4() ))

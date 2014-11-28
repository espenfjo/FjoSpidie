import logging
import tempfile
import pcap
import subprocess
import threading
from fjospidie.Utils import get_md5

class PcapEngine(threading.Thread):

    def __init__(self, spidie, pcap_folder):
        threading.Thread.__init__(self)
        self.pcap_path = None
        self.spidie = spidie
        self.pcap_folder = pcap_folder

    def run(self):
        logging.info("Starting PCAP engine")
        self.p = pcap.pcapObject()
        snaplen = 64 * 1024
        timeout = 1
        if 'bpf' in self.spidie.config:
            bpf = "{} and not (host {} and port {})".format(
                self.spidie.config.bpf, self.spidie.config.database_host, self.spidie.config.database_port)
        else:
            bpf = "not (host {} and port {})".format(self.spidie.config.database_host, self.spidie.config.database_port)

        pcap_file = tempfile.NamedTemporaryFile(prefix="suricata", suffix="pcap", delete=False, dir=self.pcap_folder)
        self.pcap_path = pcap_file.name
        logging.debug("PCAPing to " + self.pcap_path)
        dev = self.find_default_adapter()
        self.p.open_live(dev, snaplen, 0, timeout)
        self.p.setfilter(bpf, 0, 0)
        dumper = self.p.dump_open(self.pcap_path)

        self.p.loop(-1, dumper)

    def find_default_adapter(self):
        route = subprocess.Popen(['/usr/bin/env', "netstat", "-rn"], stdout=subprocess.PIPE)
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
        """
        Stop the tcpdump
        """
        self.p.breakloop()
        self.add_to_db()

    def add_to_db(self):
        """
        Add the pcap to the mongodb gridfs store
        """
        pcap_data = None
        with open(self.pcap_path, mode='rb') as f:
            pcap_data = f.read()
        logging.debug("Adding " + self.pcap_path + " to database")
        md5 = get_md5(pcap_data)
        fs_id = None
        if not self.spidie.database.fs.exists({"md5":md5}):
            fs_id = self.spidie.database.fs.put(pcap_data, type="pcap")
        else:
            grid_file = self.spidie.database.fs.get_version(md5=md5)
            fs_id = grid_file._id
        self.spidie.report.pcap_id = fs_id

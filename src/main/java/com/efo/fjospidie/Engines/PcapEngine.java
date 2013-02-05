package com.efo.fjospidie.engines;

import java.io.BufferedInputStream;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.sql.SQLException;

import org.jnetpcap.Pcap;
import org.jnetpcap.PcapBpfProgram;
import org.jnetpcap.PcapDumper;
import org.jnetpcap.PcapHandler;

import com.efo.fjospidie.FjoSpidie;
import com.efo.fjospidie.LOG;
import com.efo.fjospidie.Report;
import com.efo.fjospidie.Util;

public class PcapEngine extends Thread {
	Pcap pcap;
	PcapDumper dumper;
	private int proxyPort;

	public PcapEngine(int proxyPort) {
		this.proxyPort = proxyPort;
	}

	public void run() {
		try {
			startEngines(proxyPort);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	public void startEngines(int proxyPort) throws IOException {
		this.proxyPort = proxyPort;

		int snaplen = 64 * 1024;
		int flags = Pcap.MODE_PROMISCUOUS;
		int timeout = 10 * 1000;
		LOG.i(this, "Starting PcapEngine");

		StringBuilder errbuf = new StringBuilder(); // For any error msgs

		String externalDevice = Util.defaultRouteAdapter();
		File pcapFile = File.createTempFile("snort", "pcap");
		FjoSpidie.pcapPath = pcapFile.getAbsolutePath();
		pcap = Pcap.openLive(externalDevice, snaplen, flags, timeout, errbuf);
	/*	PcapBpfProgram bpf = new PcapBpfProgram();
		String str = "host localhost and port " + proxyPort;
		LOG.i(this, "PCAP filter: " + str);
		if (pcap.compile(bpf, str, 0, 0xFFFFFF00) != Pcap.OK) {
			System.err.println(pcap.getErr());
			return;
		}
		if (pcap.setFilter(bpf) != Pcap.OK) {
			System.err.println(pcap.getErr());
		}*/
		dumper = pcap.dumpOpen(FjoSpidie.pcapPath); // output
		pcap.loop(Pcap.LOOP_INFINITE, dumper);

	}

	public void stopEngine() {
		LOG.i(this, "Stopping PcapEngine");
		addToDB();
		pcap.breakloop();
		dumper.close(); // Won't be able to delete without explicit close
		pcap.close();
		this.interrupt();
	}

	public void compileFilter() {

	}

	public void addToDB() {
		File pcap = new File(FjoSpidie.pcapPath);
		try {

			DataInputStream dis = new DataInputStream(new BufferedInputStream(new FileInputStream(pcap)));
			Report.insertPcap(dis);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
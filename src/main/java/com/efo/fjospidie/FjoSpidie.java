package com.efo.fjospidie;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.MalformedURLException;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Random;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import org.apache.commons.cli.PosixParser;
import org.browsermob.core.har.HarEntry;
import org.browsermob.core.har.HarLog;
import org.browsermob.core.har.HarNameValuePair;

import com.efo.fjospidie.engines.PcapEngine;
import com.efo.fjospidie.engines.snort.SnortEngine;
import com.efo.fjospidie.grapher.GraphViz;
import com.efo.fjospidie.grapher.PaintGraphViz;

/**
 * 
 * @author Espen Fjellvær Olsen
 */
public class FjoSpidie {

	public static ArrayList<Connection> connections = new ArrayList<Connection>();
	public static ArrayList<Node> nodes = new ArrayList<Node>();

	static boolean debug = false;

	// TODO random path
	public static String pcapPath;
	static File pcapFile;
	static Report report;
	public static String snortConfig;
	private static String configFile = "fjospidie.conf";
	public static Configuration configuration;

	public static void main(String[] args) throws IOException {
		SnortEngine snort = null;
		// TODO LOGGER
		// TODO JavaDOC

		initialiseConfiguration(args);
		Random randi = new Random();
		int proxyPort = randi.nextInt(65534 - 20000 + 1) + 20000;
		PcapEngine pcap = null;
		GraphViz gv = new GraphViz("dot");

		Date date = new Date();
		Timestamp timestamp = new Timestamp(date.getTime());

		URL startURL = new URL(configuration.getUrl());

		try {
			report = new Report(timestamp, startURL.uri);

			pcap = new PcapEngine(proxyPort);
			pcap.start();
		} catch (SQLException e1) {
			e1.printStackTrace();
		}

		nodes.add(new Node(startURL.host));
		nodes.get(0).setStatus(200);
		gv.addln(gv.start_graph());

		WebRunner runner = new WebRunner();

		HarLog log = WebRunner.runWebDriver(startURL, proxyPort);
		pcap.stopEngine();

		if (log != null) {
			List<String> connections = runner.findExternalConnections(log);

			snort = new SnortEngine(connections);
			// List<String> cakes = new ArrayList<String>();
			// cakes.add("81.93.163.115");
			// SnortEngine snort = new SnortEngine(cakes);
			snort.start();

			List<HarEntry> entries = log.getEntries();

			// JavaScriptAnalyser jas = new JavaScriptAnalyser(entries);
			// jas.start();
			try {
				Report.insertEntries(entries);
			} catch (SQLException e) {
				e.printStackTrace();
			}
			calculateNodes(entries);
			fillNodes(gv);
		}
		PaintGraphViz.paintGraphviz(gv, nodes);

		try {
			snort.join();
			Date endOfDays = new Date();
			Timestamp endstamp = new Timestamp(endOfDays.getTime());
			Report.insertp("UPDATE report set endtime=? where id=" + Report.id, endstamp);

		} catch (SQLException es) {
			es.printStackTrace();
		} catch (InterruptedException fe) {
			fe.printStackTrace();
		}

		LOG.i(FjoSpidie.class, "Done");

		return;
	}

	private static void initialiseConfiguration(String[] args) {

		CommandLine cmd = null;
		Options options = new Options();
		options.addOption("u", "url", true, "Url of site to scan");
		options.addOption("s", "snortconf", true, "Snort configuration file");
		options.addOption("c", "configurationfile", true, "FjoSpidie configuration file");
		options.addOption("f", "firefoxprofile", true, "FjoSpidie Firefox Profile directory");
		options.addOption("u", "uuid", true, "UUID of report");


		CommandLineParser parser = new PosixParser();
		try {
			cmd = parser.parse(options, args);
			if (cmd.getOptionValue("url") == null) {
				throw new ParseException("Missing required argument url");
			}
		} catch (ParseException e2) {
			usage(options);
			e2.printStackTrace();
			System.exit(1);
		}

		if (cmd.getOptionValues("configurationfile") != null) {
			configFile = cmd.getOptionValue("configurationfile");
		}
		
		
		
		
		try {
			configuration = ConfigurationReader.readConfiguration(configFile);
		} catch (FileNotFoundException e) {
			LOG.i(FjoSpidie.class, "Could not read configuration file: " + configFile);
			e.printStackTrace();
			System.exit(1);
		}

		if (cmd.getOptionValue("snortconf") != null) {
			configuration.setSnortconf(cmd.getOptionValue("snortconf"));
		}
		configuration.setUUID(cmd.getOptionValue("uuid"));
		configuration.setUrl(cmd.getOptionValue("url"));
		

	}

	/**
	 * @param options
	 */
	private static void usage(Options options) {

		// Use the inbuilt formatter class
		HelpFormatter formatter = new HelpFormatter();
		formatter.printHelp("FjoSpidie", options);
	}

	/**
	 * Loops through a list of {@link com.efo.fjospidie.Node} objects and adds
	 * them to the {@link com.efo.FjoSpidie.GraphViz} object.
	 * 
	 * @param gv
	 *            {@link com.efo.FjoSpidie.GraphViz} object which to add nodes
	 *            to.
	 * @param nodes
	 */
	private static void fillNodes(GraphViz gv) {
		for (Node node : nodes) {
			gv.addln(node.getDOT());
		}
	}

	/**
	 * This function loops through all HTTP connections and maps all
	 * {@link com.efo.fjospidie.Node}s and {@link com.efo.fjospidie.ParentNode}
	 * s. If the response header has a 301/302 (rewrite/redirect) we add the
	 * Location as a {@link com.efo.fjospidie.Node}, and sets the
	 * {@link com.efo.fjospidie.Node} from the Host header as its parent.
	 * 
	 * All entries have at least one Host header. Add it to the Nodes list if it
	 * is not there already (For example from a previous Location header).
	 * 
	 * If we have a referrer header, find its {@link com.efo.fjospidie.Node} and
	 * set it as parent for this {@link com.efo.fjospidie.Node} unless we
	 * already have this {@link com.efo.fjospidie.Node} from a previous Location
	 * header. Should always have its parent in the Node list.
	 * 
	 * 
	 * @param entries
	 *            {@link HarEntry}
	 * @throws MalformedURLException
	 */
	private static void calculateNodes(List<HarEntry> entries) {
		for (HarEntry entry : entries) {
			Node node = null;
			int status = entry.getResponse().getStatus();

			List<HarNameValuePair> headers = entry.getRequest().getHeaders();
			headers.addAll(entry.getResponse().getHeaders());

			for (HarNameValuePair harHeader : headers) {
				if (harHeader.getName().equals("Location")) {
					if (status == 301 || status == 302) {
						java.net.URL locationURL;
						try {
							locationURL = new java.net.URL(harHeader.getValue());

							Node locationNode = new Node(locationURL.getHost());
							locationNode.setStatus(status);
							locationNode.setParent(node, status);
							addNodeIfNotExists(locationNode, entry);
						} catch (MalformedURLException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}

					} else {
						LOG.i(FjoSpidie.class, "Unknown status " + status + " when having Location header: "
								+ harHeader.getValue());
					}
				} else if (harHeader.getName().equals("Host")) {

					node = new Node(harHeader.getValue());
					node.setStatus(status);
					Node n;
					if ((n = addNodeIfNotExists(node, entry)) != null)
						node = n;

				} else if (harHeader.getName().equals("Referer")) {

					java.net.URL refURL;
					try {
						refURL = new java.net.URL(harHeader.getValue());

						for (Node pNode : nodes) {
							if (refURL.getHost().equals(pNode.getLabel())) {
								if (node.getParents().size() == 0)
									node.setParent(pNode, status);
							}
						}
					} catch (MalformedURLException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				}
			}
		}
	}

	/**
	 * Adds a {@link com.efo.fjospidie.Node} to the Node list if it already is
	 * not in the list.
	 * 
	 * @param node
	 *            The {@link com.efo.fjospidie.Node} to add to the Node list.
	 * @param entry
	 * @return Returns the already existing {@link com.efo.fjospidie.Node if the
	 *         {@link com.efo.fjospidie.Node} already exists from before.
	 * 
	 */
	private static Node addNodeIfNotExists(Node node, HarEntry entry) {
		boolean alreadyExisting = false;
		for (Node n : nodes) {
			// We have seen this connection earlier
			if (n.getLabel().equals(node.getLabel())) {
				alreadyExisting = true;
				node = n;
				return node;
			}
		}
		if (alreadyExisting == false) {
			node.setHarEntry(entry);
			node.setId(nodes.size() + 1);
			nodes.add(node);
		}

		return null;
	}

}

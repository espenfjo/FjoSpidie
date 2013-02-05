package com.efo.fjospidie.grapher;

import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;

import com.efo.fjospidie.LOG;
import com.efo.fjospidie.Node;
import com.efo.fjospidie.ParentNode;
import com.efo.fjospidie.Report;

public class PaintGraphViz {
	static HashMap<Integer, String> colours = new HashMap<Integer, String>();

	static {

		colours.put(200, "green");
		colours.put(204, "green");
		colours.put(404, "red");
		colours.put(301, "orange");
		colours.put(302, "yellow");
		colours.put(304, "yellow");

	}

	public static void paintGraphviz(GraphViz gv, ArrayList<Node> nodes) {

		gv.addln("graph [ratio=fill];");
		gv.addln("graph [rankdir=LR];");
		gv.addln("graph [bb=\"0,0,1382,108\"];");
		gv.addln(nodes.get(0).getDOT());

		for (Node node : nodes) {
			// Does this node have any parent connections?
			if (node.getParents().size() > 0) {
				for (ParentNode parentNode : node.getParents()) {
					String color = colours.get(parentNode.getStatus());
					double edgeWeight = 1 + (0.1 * parentNode.getNumberOfLinks());
					String link = "[color=" + color + " penwidth=" + edgeWeight + "]";
					// Add connection from parent (referrer or Location) to this node
					gv.addln(parentNode.getNode() + " -> " + node.getNode() + " " + link);
				}
			} else {
				gv.addln(nodes.get(0).getNode() + " -> " + node.getNode());
			}
		}

		gv.addln(gv.end_graph());
		LOG.d(gv.getDotSource());
		String type = "png";
		File out = new File("/Users/Espen/Desktop/graph." + type);
		byte img[] = gv.getGraph(gv.getDotSource(), type);

		Report.writeImg(img);
		gv.writeGraphToFile(gv.getGraph(gv.getDotSource(), type), out);
	}

}

package com.efo.fjospidie;

import java.util.ArrayList;
import java.util.List;

import org.browsermob.core.har.HarEntry;


public class Node {

	private int status;
	private String label;
	private List<ParentNode> parents = new ArrayList<ParentNode>();
	private int id;
	private HarEntry harEntry;

	/**
	 * @param hostName
	 */
	public Node(String hostName) {
		this.label = hostName;
	}

	/**
	 * @return
	 */
	public int getStatus() {
		return status;
	}

	/**
	 * @param type
	 */
	public void setStatus(int type) {
		this.status = type;
	}

	/**
	 * @return
	 */
	public String getLabel() {
		return label;
	}

	/**
	 * @param label
	 */
	public void setLabel(String label) {
		this.label = label;
	}

	/**
	 * @return
	 */
	public List<ParentNode> getParents() {
		return parents;
	}

	/**
	 * @param parent
	 * @param status
	 */
	public void setParent(Node parent, int status) {
		ParentNode node = new ParentNode(parent.getLabel());
		node.setId(parent.getId());
		node.setStatus(status);
		boolean alreadyExists = false;
		for (ParentNode existingPnode : parents) {
			// Does new parent match old parent? Aka have we had this connection
			// earlier
			if (existingPnode.getLabel().equals(node.getLabel())) {
				// We have an old connection, but do we have an old connection
				// with the same HTTP status code (OK, REDIRECT etc)?
				if (status == getStatus()) {
					existingPnode.incrementNumberOfLinks();
					alreadyExists = true;
					break;
				}
			}
		}
		if (!alreadyExists) {
			this.parents.add(node);
		}
	}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getDOT() {
		return "node" + id + " [label=\"" + label + "\"]";
	}

	public String getNode() {
		String node = "node" + id;
		return node;
	}

	public HarEntry getHarEntry() {
		return harEntry;
	}

	public void setHarEntry(HarEntry harEntry) {
		// TODO Auto-generated method stub
		this.harEntry = harEntry;
	}
}

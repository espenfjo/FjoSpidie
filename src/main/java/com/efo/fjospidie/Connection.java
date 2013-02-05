package com.efo.fjospidie;

import java.net.InetAddress;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.List;

public class Connection {

	private Connection parent;
	private List<Connection> children;
	private String dns;
	private String ip;
	private java.net.URL referer;

	public Connection(InetAddress addr) {
		this.dns = addr.getHostName();
		this.ip = addr.getHostAddress();

		for (Connection connection : FjoSpidie.connections) {
			if (connection.getDns().equals(this.dns)) {
				return;
			} // else if

		}

	}

	public Connection getParent() {
		return parent;
	}

	public void setParent(String string) {
	/*	for (Connection connection : FjoSpidie.connections) {
			if(connection.getDns().equals(anObject))
		}
		this.parent = string;
	*/}

	public List<Connection> getChildren() {
		return children;
	}

	public void setChildren(List<Connection> children) {
		this.children = children;
	}

	public String getDns() {
		return dns;
	}

	public void setDns(String dns) {
		this.dns = dns;
	}

	public String getIp() {
		return ip;
	}

	public void setIp(String ip) {
		this.ip = ip;
	}

	public int getNumOfChildren() {
		return children.size();
	}

	public List<Connection> getSiblings() {
		if (parent.getNumOfChildren() <= 0)
			return null;

		List<Connection> parentsChildren = parent.getChildren();
		parentsChildren.remove(this);
		return parentsChildren;

	}

	public java.net.URL getReferer() {
		return referer;
	}

	public void setReferer(String referer) {
		java.net.URL ref = null;
		try {
			ref = new URL(referer);
		} catch (MalformedURLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		this.referer = ref;
	}
}

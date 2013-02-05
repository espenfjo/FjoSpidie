package com.efo.fjospidie;

/**
 * @author espen
 *
 */
public class ParentNode extends Node {
	private int numberOfLinks = 1;

	/**
	 * @param hostName
	 */
	public ParentNode(String hostName) {
		super(hostName);
	}

	/**
	 * @return
	 */
	public int getNumberOfLinks() {
		return numberOfLinks;
	}

	
	
	/**
	 * 
	 */
	public void incrementNumberOfLinks() {
		this.numberOfLinks++;
	}

}

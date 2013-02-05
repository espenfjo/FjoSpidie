package com.efo.fjospidie;

import java.net.MalformedURLException;
import java.util.ArrayList;
import java.util.List;

import org.openqa.selenium.WebElement;

public class URL implements Comparable<URL> {

	int seen;
	java.net.URL url;
	List<URL> references = new ArrayList<URL>();
	WebElement element;
	String uri;
	String host;
	String protocol;
	public List<String> includes = new ArrayList<String>();

	public URL(String string) {
		if (string != null && string.contains("javascript")) {
			this.uri = string;
			this.protocol = "javascript";

		} else {

			java.net.URL url = null;
			try {
				url = new java.net.URL(string);
			} catch (MalformedURLException e) {
				System.out.println("Couldnt convert: " + string);
				e.printStackTrace();
			}

			if (url != null) {
				this.url = url;
				this.protocol = url.getProtocol();
				this.host = url.getHost();
				this.uri = url.toString();
			}
		}
	}

	public WebElement getElement() {
		return element;
	}

	public void element(WebElement element) {
		this.element = element;
		String href = element.getAttribute("href").toString();
		try {
			this.url = new java.net.URL(href);
		} catch (MalformedURLException e) {
			e.printStackTrace();
		}
	}

	public void click() {
		LOG.d("Clicking on " + uri + "\n");
		if (element != null)
			element.click();
		else
			WebRunner.driver.get(uri);
	}

	public int compareTo(URL o) {
		return o.seen - this.seen;
	}

	public int seen() {
		return seen;
	}

	public void seen(int seen) {
		this.seen = seen;
	}

	public String uri() {
		return uri;
	}

	public void uri(String uri) {
		this.uri = uri;
	}

	public List<URL> references() {
		return references;
	}

	public List<String> includes() {
		return includes;
	}
	/*
	 * public static Comparator<URL> sortByReferences = new Comparator<URL>() {
	 * 
	 * public int compare(URL url1, URL url2) {
	 * 
	 * String fruitName1 = url1.getFruitName().toUpperCase(); String fruitName2
	 * = url2.getFruitName().toUpperCase();
	 * 
	 * // ascending order return fruitName1.compareTo(fruitName2);
	 * 
	 * // descending order // return fruitName2.compareTo(fruitName1); }
	 * 
	 * };
	 */
}
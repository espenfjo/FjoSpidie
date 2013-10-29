package com.efo.fjospidie;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.attribute.FileAttribute;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

import org.apache.http.HttpRequestInterceptor;
import org.browsermob.core.har.Har;
import org.browsermob.core.har.HarEntry;
import org.browsermob.core.har.HarLog;
import org.browsermob.proxy.ProxyServer;
import org.browsermob.proxy.http.BrowserMobHttpRequest;
import org.browsermob.proxy.http.RequestInterceptor;
import org.openqa.selenium.By;
import org.openqa.selenium.Proxy;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxProfile;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.remote.CapabilityType;
import org.openqa.selenium.remote.DesiredCapabilities;

public class WebRunner {
	private static int recursionLevel = 0;
	private static int wantedRecrusionLevel = 1000;
	static WebDriver driver;
	public static ArrayList<com.efo.fjospidie.URL> URLs = new ArrayList<com.efo.fjospidie.URL>();
	static List<String> whiteDomains = Arrays.asList("google.com");
	static List<String> protocols = Arrays.asList("http", "https", "javascript");
	static List<String> stfuDomains = Arrays.asList("http", "https");

	static boolean one = true;
	static URL currentPage;
	static boolean firstRequest = false;
        static String referer = "http://www.google.com/search?q=hei+&oq=SUP&sourceid=firefox&ie=UTF-8";
        static String useragent = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2b5) Gecko/20091204 Firefox/3.6b5 Java/1.7.0_11";
	static HarLog runWebDriver(URL startURL, int port) {
		LOG.i(WebRunner.class, "Starting WebRunner");
		if ( FjoSpidie.configuration.getReferer() != null ) {
		        referer = FjoSpidie.configuration.getReferer();
		}
		if ( FjoSpidie.configuration.getUserAgent() != null ) {
		        useragent = FjoSpidie.configuration.getUserAgent();
		}

		
		ProxyServer server = new ProxyServer(port);
		
		try {
			server.start();
			server.setCaptureHeaders(true);
			server.setCaptureContent(false);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		server.addHeader("User-Agent", useragent);
		server.addHeader("Accept-Encoding", "");
		RequestInterceptor interceptor = new RequestInterceptor() {
			public void process(BrowserMobHttpRequest arg0) {
				if (firstRequest == false) {
				        arg0.addRequestHeader("Referer", referer);							
					firstRequest = true;
				}
			}
		};
		server.addRequestInterceptor(interceptor);

		FirefoxProfile fp = null;
		File profile = null;
		try {
			profile = new File(FjoSpidie.configuration.getFirefoxProfile());
		} catch (NullPointerException e) {
		}
		if (profile != null && profile.exists()) {
			fp = new FirefoxProfile(profile);
		} else {
			fp = new FirefoxProfile();
		}

		Path downloadDir;
		try {
			downloadDir = Files.createTempDirectory("spidie");
		} catch (IOException e2) {
			e2.printStackTrace();
			return null;
		}

		fp.setPreference("security.OCSP.enabled", 0);
		fp.setPreference("browser.download.folderList", 2);
		fp.setPreference("browser.download.manager.showWhenStarting", false);
		fp.setPreference("browser.download.dir", downloadDir.toString());
		fp.setPreference(
				"browser.helperApps.neverAsk.saveToDisk",
				"application/x-xpinstall;application/x-zip;application/x-zip-compressed;application/octet-stream;application/zip;application/pdf;application/msword;text/plain;application/octet");
		fp.setPreference("browser.helperApps.alwaysAsk.force", false);
		fp.setPreference("browser.download.manager.showWhenStarting", false);
		fp.setPreference("network.proxy.http", "localhost");
		fp.setPreference("network.proxy.http_port", server.getPort());

		fp.setPreference("network.proxy.type", 1);
		driver = new FirefoxDriver(fp);

		one = true;
		server.newHar(startURL.host);
		analysePage(startURL);
		driver.close();

		Har har = server.getHar();
		try {
			server.stop();
		} catch (Exception e) {
			e.printStackTrace();
		}
		// TODO Add HAR to database
		HarLog log = null;
		log = har.getLog();

		LOG.i(WebRunner.class, "Stopping WebRunner");
		DownloadManager dm = new DownloadManager();
		try {
			dm.storeDownload(downloadDir);
		} catch (Exception e) {
			e.printStackTrace();
		}

		return log;

	}

	static void enumerateLinks(URL URL) {

		URL link;
		LOG.d("Clicking on: " + URL.uri);
		URL.click();
		currentPage = new URL(driver.getCurrentUrl());
		URLs.add(currentPage);
		// verifyContent();
		recursionLevel++;
		while ((link = findFirstUnvistedLink(currentPage)) != null) {
			if (recursionLevel > wantedRecrusionLevel) {
				System.out.println("O HAI BREAKS");
				break;
			}
			enumerateLinks(link);
			recursionLevel--;
		}
		driver.navigate().back();
		LOG.d("Navigated back to: " + driver.getCurrentUrl());
	}

	static com.efo.fjospidie.URL findFirstUnvistedLink(URL currentPage) {
		List<WebElement> links = driver.findElements(By.tagName("a"));
		links: for (WebElement link : links) {

			URL url = new URL(link.getAttribute("href"));
			for (URL alreadyExisting : URLs) {
				if (alreadyExisting.uri.equals(url.uri)) {
					// LOG.d("Found " + url.uri + "which is already visited\n");
					alreadyExisting.seen++;
					alreadyExisting.references.add(currentPage);
					continue links;
				}
			}
			if (!protocols.contains(url.protocol)) {
				LOG.d("Skipping " + url.uri + " because of silly protocol " + url.protocol);
				continue;
			}
			boolean okDomain = false;
			for (String whitedomain : whiteDomains) {
				if (url.host != null && !url.host.matches("([^/@]*\\.)?" + whitedomain)) {
					// LOG.d("Skipping " + url.host +
					// " because of silly domain not being " + whitedomain);
					okDomain = false;
				} else {
					LOG.d("url " + url.uri + " matches " + whitedomain);
					okDomain = true;
					break;
				}
			}
			if (okDomain)
				return url;
		}

		return null;
	}

	private static void analysePage(URL url) {
		url.click();
		currentPage = new URL(driver.getCurrentUrl());
		//enumerateLinks(currentPage);
		// verifyContent();
		URLs.add(currentPage);
		LOG.i(WebRunner.class, "Refreshing page");

	}

	private static void verifyContent() {

		findExternalSources();
		findJavascriptHref();
		findFlash();
	}

	private static void findFlash() {
		List<WebElement> objects = driver.findElements(By.tagName("object"));
		// TODO Auto-generated method stub
		for (WebElement webElement : objects) {
			List<WebElement> moreObjects = webElement.findElements(By.tagName("object"));
			moreObjects.addAll(webElement.findElements(By.tagName("embed")));

			String attribute = webElement.getAttribute("type");
			if (attribute != null) {
				if (attribute.matches(".*flash.*")) {
					String data = webElement.getAttribute("data");
					if (data != null) {
						currentPage.includes.add(data);
						LOG.d("Adding flash " + data);
					}
				}

			}
		}
	}

	private static void findJavascriptHref() {
		List<WebElement> hrefs = driver.findElements(By.xpath("//*[@href]"));
		for (WebElement js : hrefs) {

			String href = js.getAttribute("href");

			if (href == null)
				continue;
			if (!href.matches("^javascript.*"))
				continue;

			currentPage.includes.add(href);
			LOG.d("Adding js " + href);
		}
	}

	private static void findExternalSources() {
		List<WebElement> sources = driver.findElements(By.xpath("//*[@src]"));
		for (WebElement src : sources) {
			String href = src.getAttribute("src");

			if (href == null)
				continue;

			currentPage.includes.add(href);
			LOG.d("Adding include " + href);
		}
	}

	List<String> findExternalConnections(HarLog log) {
		List<String> connections = new ArrayList<String>();
		HAR: for (HarEntry entry : log.getEntries()) {
			if (entry.getServerIPAddress() != null) {
				for (String oldConnections : connections)
					if (oldConnections.equals(entry.getServerIPAddress()))
						continue HAR;

				connections.add(entry.getServerIPAddress());
			}
		}
		System.out.println(connections.toString());
		return connections;
	}

}

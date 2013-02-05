package com.efo.fjospidie;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.SocketException;
import java.util.Enumeration;
import java.util.NoSuchElementException;
import java.util.StringTokenizer;

public class Util {

	public void outsideIP() {
		String ip;
		try {
			Enumeration<NetworkInterface> interfaces = NetworkInterface.getNetworkInterfaces();
			while (interfaces.hasMoreElements()) {
				NetworkInterface iface = interfaces.nextElement();
				// filters out 127.0.0.1 and inactive interfaces
				if (iface.isLoopback() || !iface.isUp())
					continue;

				Enumeration<InetAddress> addresses = iface.getInetAddresses();
				while (addresses.hasMoreElements()) {
					InetAddress addr = addresses.nextElement();
					ip = addr.getHostAddress();
					System.out.println(iface.getDisplayName() + " " + ip);
				}
			}
		} catch (SocketException e) {
			throw new RuntimeException(e);
		}
	}

	public static String defaultRouteAdapter() throws IOException {
		Process result = Runtime.getRuntime().exec("netstat -rn");

		BufferedReader output = new BufferedReader(new InputStreamReader(result.getInputStream()));

		String line = output.readLine();
		while (line != null) {
			if (line.startsWith("default") == true || line.startsWith("0.0.0.0") == true)
				break;
			line = output.readLine();
		}

		StringTokenizer st = new StringTokenizer(line);
		st.nextToken();
		String gateway = st.nextToken();

		st.nextToken();
		st.nextToken();
		st.nextToken();

		String adapter = st.nextToken();
		try {
			st.nextToken();
			String linuxAdapter = st.nextToken();
			adapter = linuxAdapter;
		} catch (NoSuchElementException e) {
		}

		return adapter;

	}
}

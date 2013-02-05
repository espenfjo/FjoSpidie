package com.efo.fjospidie;

import java.io.DataInputStream;
import java.net.MalformedURLException;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Connection;
import java.sql.Timestamp;
import java.util.List;

import org.browsermob.core.har.HarEntry;
import org.browsermob.core.har.HarNameValuePair;
import org.browsermob.core.har.HarRequest;
import org.browsermob.core.har.HarResponse;

import com.efo.fjospidie.engines.snort.SnortAlert;

public class Report {
	String database = FjoSpidie.configuration.getDatabase();
	String databaseHost = FjoSpidie.configuration.getDatabaseHost();
	String databasePort = FjoSpidie.configuration.getDatabasePort();
	String databaseUser = FjoSpidie.configuration.getDatabaseUser();
	String databasePassword = FjoSpidie.configuration.getDatabasePassword();

	String cstring = "jdbc:mysql://" + databaseHost + ":" + databasePort + "/" + database
			+ "?rewriteBatchedStatements=true";

	static Connection con = null;
	public static int id;

	public Report(Timestamp timestamp, String url) throws SQLException {
		String uuid;
		if (FjoSpidie.configuration.getUUID() != null) {
			uuid = FjoSpidie.configuration.getUUID();
		} else {
			uuid = java.util.UUID.randomUUID().toString();
		}
		con = DriverManager.getConnection(cstring, databaseUser, databasePassword);
		PreparedStatement pst = null;

		pst = con.prepareStatement("INSERT INTO report (starttime, url,uuid) VALUES (?,?,?)",
				Statement.RETURN_GENERATED_KEYS);

		pst.setTimestamp(1, timestamp);
		pst.setString(2, url);
		pst.setString(3, uuid);
		pst.executeUpdate();
		ResultSet rs = pst.getGeneratedKeys();

		rs.next();
		id = Integer.parseInt(rs.getString(1));

	}

	public static ResultSet insert(String query) throws SQLException {

		Statement st = con.createStatement();
		LOG.d("Query: " + query);
		st.executeUpdate(query, Statement.RETURN_GENERATED_KEYS);
		return st.getGeneratedKeys();

	}

	public static ResultSet insertp(String query, Object... objects) throws SQLException {
		PreparedStatement pst = null;
		pst = con.prepareStatement(query, Statement.RETURN_GENERATED_KEYS);

		for (int i = 0; i < objects.length; i++) {
			if (objects[i].getClass().equals(Integer.TYPE)) {
				pst.setInt(i + 1, (Integer) objects[i]);
			} else if (objects[i].getClass().equals(String.class)) {
				pst.setString(i + 1, (String) objects[i]);

			} else if (objects[i].getClass().equals(Timestamp.class)) {
				pst.setTimestamp(i + 1, (Timestamp) objects[i]);

			}
		}
		pst.executeUpdate();

		LOG.d("Query: " + query);

		return pst.getGeneratedKeys();

	}

	public static void addAlert(SnortAlert alert) throws SQLException {
		PreparedStatement pst = null;
		pst = con
				.prepareStatement("INSERT INTO alert (report_id, alarm_text, classification, priority, to_ip,from_ip) VALUES(?,?,?,?,?,?)");
		pst.setInt(1, id);
		pst.setString(2, alert.getAlarm_text());
		pst.setString(3, alert.getClassification());
		pst.setInt(4, alert.getPriority());
		pst.setString(5, alert.getSrc());
		pst.setString(6, alert.getDst());

		pst.executeUpdate();
		LOG.d("Query: " + pst.toString());
	}

	public static void writeImg(byte[] img) {
		PreparedStatement pst = null;
		try {
			pst = con.prepareStatement("INSERT INTO graph (report_id,graph) VALUES(?,?)");
			pst.setInt(1, id);
			pst.setBytes(2, img);
			pst.executeUpdate();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	public static void insertEntries(List<HarEntry> entries) throws SQLException {
		int entryId = 0;
		PreparedStatement headerPST = null;
		headerPST = con.prepareStatement("INSERT INTO header" + " (entry_id,name,value,type) VALUES(?,?,?,?)");

		for (HarEntry entry : entries) {
			ResultSet rs;
			rs = insert("INSERT INTO entry (report_id) values(" + id + ")");
			rs.next();
			entryId = Integer.parseInt(rs.getString(1));

			if (entryId <= 0)
				continue;

			HarRequest harRequest = entry.getRequest();
			HarResponse harResponse = entry.getResponse();
			java.net.URL url = null;
			try {
				url = new java.net.URL(harRequest.getUrl());
			} catch (MalformedURLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
				LOG.d(harRequest.toString());
			}

			if (url != null) {

				insertResponse(entryId, harResponse);
				insertRequest(entryId, harRequest, url.getHost());

				for (HarNameValuePair header : harResponse.getHeaders()) {
					headerPST = insertHeader(header, "response", entryId, headerPST);
				}
				for (HarNameValuePair header : harRequest.getHeaders()) {
					headerPST = insertHeader(header, "request", entryId, headerPST);
				}
			}
		}
		headerPST.executeBatch();
	}

	private static PreparedStatement insertHeader(HarNameValuePair header, String type, int hid, PreparedStatement pst) {
		try {
			pst.setInt(1, hid);
			pst.setString(2, header.getName());
			pst.setString(3, header.getValue());
			pst.setString(4, type);
			LOG.d(pst.toString());
			pst.addBatch();

		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return pst;
	}

	private static PreparedStatement insertResponse(int entryId, HarResponse harResponse) throws SQLException {

		PreparedStatement pst = con
				.prepareStatement(
						"INSERT INTO response (entry_id,httpVersion,statusText,status,bodySize,headerSize) VALUES(?,?,?,?,?,?)",
						Statement.RETURN_GENERATED_KEYS);
		pst.setInt(1, entryId);
		pst.setString(2, harResponse.getHttpVersion());
		pst.setString(3, harResponse.getStatusText());
		pst.setInt(4, harResponse.getStatus());
		pst.setLong(5, harResponse.getBodySize());
		pst.setLong(6, harResponse.getHeadersSize());
		LOG.d("Query: " + pst.toString());
		pst.executeUpdate();
		return pst;

	}

    private static PreparedStatement insertRequest(int entryId, HarRequest harRequest, String host) throws SQLException {
		PreparedStatement pst = null;
		pst = con.prepareStatement(
				"INSERT INTO request (entry_id,httpVersion,method,uri,bodySize,headerSize, host) VALUES(?,?,?,?,?,?,?)",
				Statement.RETURN_GENERATED_KEYS);
		pst.setInt(1, entryId);
		pst.setString(2, harRequest.getHttpVersion());
		pst.setString(3, harRequest.getMethod());
		pst.setString(4, harRequest.getUrl());
		pst.setLong(5, harRequest.getBodySize());
		pst.setLong(6, harRequest.getHeadersSize());
		pst.setString(7, host);
		LOG.d("Query: " + pst.toString());
		pst.executeUpdate();
		return pst;

	}

	public static void insertPcap(DataInputStream dis) throws SQLException {
		PreparedStatement pst = null;
		String uuid = java.util.UUID.randomUUID().toString();

		try {
			pst = con.prepareStatement("INSERT INTO pcap" + " (report_id,data,uuid) VALUES(?,?,?)");

			pst.setInt(1, id);
			pst.setBinaryStream(2, dis);
			pst.setString(3, uuid);
			LOG.d(pst.toString());
			pst.executeUpdate();

		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public static void insertDownload(DataInputStream dis, String md5, String sha1, String sha256, String fileName,
			long fileSize) throws SQLException {
		String uuid = java.util.UUID.randomUUID().toString();

		PreparedStatement pst = null;
		try {
			pst = con.prepareStatement("INSERT INTO download"
					+ " (report_id,data,md5,sha1,sha256,filename,size,uuid) VALUES(?,?,?,?,?,?,?,?)");

			pst.setInt(1, id);
			pst.setBinaryStream(2, dis);
			pst.setString(3, md5);
			pst.setString(4, sha1);
			pst.setString(5, sha256);
			pst.setString(6, fileName);
			pst.setLong(7, fileSize);
			pst.setString(8, uuid);

			LOG.d(pst.toString());
			pst.executeUpdate();

		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
}

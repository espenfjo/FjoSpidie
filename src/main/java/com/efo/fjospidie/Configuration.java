package com.efo.fjospidie;

public class Configuration {

	private String snortConfig;
	private String databaseHost;
	private String databaseUser;
	private String databasePassword;
	private String databasePort;
	private String database;
	private String url;
	private String firefoxProfile;
	private String UUID;

	public void setSnortconf(String snortConfig) {
		this.snortConfig = snortConfig;
	}

	public String getSnortConfig() {
		return snortConfig;
	}

	public void setSnortConfig(String snortConfig) {
		this.snortConfig = snortConfig;
	}

	public String getDatabaseHost() {
		return databaseHost;
	}

	public void setDatabaseHost(String databaseHost) {
		this.databaseHost = databaseHost;
	}

	public String getDatabaseUser() {
		return databaseUser;
	}

	public void setDatabaseUser(String databaseUser) {
		this.databaseUser = databaseUser;
	}

	public String getDatabasePassword() {
		return databasePassword;
	}

	public void setDatabasePassword(String databasePassword) {
		this.databasePassword = databasePassword;
	}

	public String getDatabasePort() {
		return databasePort;
	}

	public void setDatabasePort(String databasePort) {
		this.databasePort = databasePort;
	}

	public String getDatabase() {
		return database;
	}

	public void setDatabase(String database) {
		this.database = database;
	}

	public String getUrl() {
		return url;
	}

	public void setUrl(String url) {
		this.url = url;
	}

	public String getFirefoxProfile() {
		return firefoxProfile;
	}

	public void setFirefoxProfile(String firefoxProfile) {
		this.firefoxProfile = firefoxProfile;
	}

	public String getUUID() {
		return UUID;
	}

	public void setUUID(String uUID) {
		UUID = uUID;
	}

}

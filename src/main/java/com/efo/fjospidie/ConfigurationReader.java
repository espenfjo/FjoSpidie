package com.efo.fjospidie;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;

import com.google.gson.Gson;

public class ConfigurationReader {

	public static Configuration readConfiguration(String configFile) throws FileNotFoundException {
		Gson gson = new Gson();
		BufferedReader bufferedReader = new BufferedReader(new FileReader(configFile));
		Configuration configuration = gson.fromJson(bufferedReader, Configuration.class);		
		return configuration;
	}

}

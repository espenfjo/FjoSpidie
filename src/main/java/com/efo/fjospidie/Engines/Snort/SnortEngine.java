package com.efo.fjospidie.engines.snort;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.ProcessBuilder.Redirect;
import java.util.ArrayList;
import java.util.List;

import com.efo.fjospidie.FjoSpidie;
import com.efo.fjospidie.LOG;
import com.efo.fjospidie.Report;

public class SnortEngine extends Thread {

	List<String> connections;
	private List<SnortAlert> alerts = new ArrayList<SnortAlert>();

	public SnortEngine(List<String> connections) {
		this.connections = connections;
	}

	public void run() {

		try {
			Process analisysProgess;
			ProcessBuilder pb;
			String EXTERNAL_NET = "[";
			for (String connection : connections) {
				if (connection != null)
					EXTERNAL_NET += connection + ",";
			}
			EXTERNAL_NET += "]";
			LOG.i(this, "Launching snort");
			String snortConfiguration = FjoSpidie.configuration.getSnortConfig();
			pb = new ProcessBuilder("snort", "-c", snortConfiguration, "-A", "console", "-q", "-N", "-r",
					FjoSpidie.pcapPath, "-S", "EXTERNAL_NET=" + EXTERNAL_NET);

			analisysProgess = pb.start();
			BufferedReader input = new BufferedReader(new InputStreamReader(analisysProgess.getInputStream()));
			StreamGobbler err = new StreamGobbler(analisysProgess.getErrorStream(), "ERROR ");
			err.start();
			String line = "";
			while ((line = input.readLine()) != null) {
				SnortAlert alert = new SnortAlert(line);
				alerts.add(alert);
				Report.addAlert(alert);

				LOG.d(alert.getAlarm_text() + " " + alert.getClassification());

			}
			int exitVal = analisysProgess.waitFor();
			LOG.i(this, "Snort stopped " + exitVal);
			LOG.i(this, "SQLifying alerts");

		} catch (Exception e) {
			e.printStackTrace();
		}

	}
}

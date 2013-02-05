package com.efo.fjospidie;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class LOG {

	private static void log(Class whom, String log) {
		Logger logger = LoggerFactory.getLogger(whom);
		logger.info(log);

	}

	public static void d(final String log) {
		if (FjoSpidie.debug)
			System.out.println(log);
	}

	public static void i(Object whom,final String log) {

		log(whom.getClass(), log);
	}
}

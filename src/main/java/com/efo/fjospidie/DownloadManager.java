package com.efo.fjospidie;

import java.io.*;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;

import org.apache.commons.codec.digest.DigestUtils;

public class DownloadManager {

	public void storeDownload(Path tempPath) throws Exception {
		LOG.i(this,"Checking dir " + tempPath.toString());
		File fp = tempPath.toFile();
		ArrayList<File> matchingFiles = new ArrayList<File>(Arrays.asList(fp.listFiles()));

		for (int i = 0; matchingFiles.size() > i; i++) {
			File file = matchingFiles.get(i);
			if (file.getName().matches("[.]part")) {
				LOG.i(this,"File " + file.getName() + " is not complete, should try it again.");
			}
			LOG.i(this,"Checking dir " + file.toString());

			InputStream fis = new FileInputStream(file);
			String sha1 = DigestUtils.shaHex(fis);
			fis = new FileInputStream(file);
			String md5 = DigestUtils.md5Hex(fis);
			fis = new FileInputStream(file);
			String sha256 = DigestUtils.sha256Hex(fis);
			long fileSize = file.length();
			LOG.d(md5);
			LOG.d(sha1);
			LOG.d(sha256);
			LOG.i(this,"Removing " + file.getName());
			matchingFiles.remove(file);
			DataInputStream dis = new DataInputStream(new BufferedInputStream(new FileInputStream(file)));
			Report.insertDownload(dis, md5, sha1, sha256, file.getName(), fileSize);

		}
	}
}

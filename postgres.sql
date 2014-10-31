CREATE TABLE report (
    id serial PRIMARY KEY,
    url text,
    starttime timestamp without time zone NOT NULL,
    endtime timestamp without time zone,
    uuid uuid
);

CREATE TABLE entry (
    id serial PRIMARY KEY,
    report_id integer NOT NULL REFERENCES report(id)
);



CREATE TABLE request (
    id serial PRIMARY KEY,
    entry_id integer REFERENCES entry(id),
    bodysize integer,
    headersize integer,
    method text,
    uri text,
    httpversion text,
    host text,
    port integer
);

CREATE TABLE alert (
    id SERIAL PRIMARY KEY,
    report_id integer NOT NULL,
    alarm_text text,
    classification text,
    priority integer,
    protocol character varying(10) DEFAULT NULL::character varying,
    from_ip text,
    to_ip text,
    request integer REFERENCES request(id),
    http_method text,
    http_request text
);

CREATE TABLE download (
    id SERIAL PRIMARY KEY,
    report_id integer NOT NULL REFERENCES report(id),
    data bytea,
    md5 text,
    sha1 text,
    sha256 text,
    size integer,
    uuid uuid,
    filename text
);




CREATE TABLE graph (
    id serial PRIMARY KEY,
    report_id integer NOT NULL references report(id),
    graph bytea
);

CREATE TABLE screenshot (
    id serial PRIMARY KEY,
    report_id integer NOT NULL references report(id),
    image bytea
);


CREATE TABLE header (
    id serial PRIMARY KEY,
    entry_id integer REFERENCES entry(id),
    name text,
    value text,
    type text
);


CREATE TABLE pcap (
    id serial PRIMARY KEY,
    report_id integer REFERENCES report(id),
    data bytea,
    uuid uuid
);



CREATE TABLE response (
    id serial PRIMARY KEY,
    entry_id integer REFERENCES entry(id),
    httpversion text,
    statustext text,
    status integer,
    bodysize integer,
    headersize integer
);

CREATE TABLE cookie (
    id serial PRIMARY KEY,
    response_id integer,
    name text,
    value bytea,
    path text,
    domain text,
    expires text,
    httpOnly text,
    secure text,
    comment text
 );
ALTER TABLE cookie ADD CONSTRAINT cookie_response_id_fkey FOREIGN KEY(response_id) REFERENCES response(id) DEFERRABLE;

CREATE TABLE response_content (
    id serial PRIMARY KEY,
    response_id integer,
    path text,
    md5 text,
    data text,
    mimetype text,
    size integer
);

ALTER TABLE response_content ADD CONSTRAINT response_content_response_id_fkey FOREIGN KEY(response_id) REFERENCES response(id) DEFERRABLE;

CREATE TABLE yara (
  id serial PRIMARY KEY,
  content_id integer REFERENCES response_content(id),
  rule text,
  description text
);

CREATE TABLE yara_tag(
  id serial PRIMARY KEY,
  yara_id integer REFERENCES yara(id),
  tag text
);

CREATE TABLE yara_string(
  id serial PRIMARY KEY,
  yara_id integer REFERENCES yara(id),
  string text
);


GRANT ALL ON TABLE alert TO fjospidie;
GRANT ALL ON SEQUENCE alert_id_seq TO fjospidie;
GRANT ALL ON TABLE download TO fjospidie;
GRANT ALL ON TABLE entry TO fjospidie;
GRANT SELECT,USAGE ON SEQUENCE entry_id_seq TO fjospidie;
GRANT ALL ON TABLE graph TO fjospidie;
GRANT SELECT,USAGE ON SEQUENCE graph_id_seq TO fjospidie;
GRANT ALL ON TABLE screenshot TO fjospidie;
GRANT SELECT,USAGE ON SEQUENCE screenshot_id_seq TO fjospidie;
GRANT ALL ON TABLE header TO fjospidie;
GRANT SELECT,USAGE ON SEQUENCE header_id_seq TO fjospidie;
GRANT ALL ON TABLE pcap TO fjospidie;
GRANT ALL ON SEQUENCE pcap_id_seq TO fjospidie;
GRANT ALL ON TABLE report TO fjospidie;
GRANT SELECT,USAGE ON SEQUENCE report_id_seq TO fjospidie;
GRANT ALL ON TABLE request TO fjospidie;
GRANT SELECT,USAGE ON SEQUENCE request_id_seq TO fjospidie;
GRANT ALL ON TABLE response TO fjospidie;
GRANT SELECT,USAGE ON SEQUENCE response_id_seq TO fjospidie;
GRANT ALL ON TABLE cookie TO fjospidie;
GRANT SELECT,USAGE ON SEQUENCE cookie_id_seq TO fjospidie;
GRANT ALL ON TABLE response_content TO fjospidie;
GRANT SELECT,USAGE ON SEQUENCE response_content_id_seq TO fjospidie;
GRANT ALL ON TABLE yara TO fjospidie;
GRANT SELECT,USAGE ON SEQUENCE yara_id_seq TO fjospidie;
GRANT ALL ON TABLE yara_string TO fjospidie;
GRANT SELECT,USAGE ON SEQUENCE yara_string_id_seq TO fjospidie;
GRANT ALL ON TABLE yara_tag TO fjospidie;
GRANT SELECT,USAGE ON SEQUENCE yara_tag_id_seq TO fjospidie;

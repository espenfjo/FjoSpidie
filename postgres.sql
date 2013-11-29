CREATE TABLE alert (
    id SERIAL PRIMARY KEY,
    report_id integer NOT NULL,
    alarm_text text,
    classification text,
    priority integer,
    protocol character varying(10) DEFAULT NULL::character varying,
    from_ip text,
    to_ip text
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


CREATE TABLE entry (
    id serial PRIMARY KEY,
    report_id integer NOT NULL REFERENCES report(id)
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


CREATE TABLE report (
    id serial PRIMARY KEY,
    url text,
    starttime timestamp without time zone NOT NULL,
    endtime timestamp without time zone,
    uuid uuid
);



CREATE TABLE request (
    id serial PRIMARY KEY,
    entry_id integer REFERENCES entry(id)
    bodysize integer,
    headersize integer,
    method text,
    uri text,
    httpversion text,
    host text,
    port integer
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

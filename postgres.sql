--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alert; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE alert (
    id integer NOT NULL,
    report_id integer NOT NULL,
    alarm_text text,
    classification text,
    priority integer,
    protocol character varying(10) DEFAULT NULL::character varying,
    from_ip text,
    to_ip text
);


ALTER TABLE public.alert OWNER TO postgres;

--
-- Name: alert_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE alert_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.alert_id_seq OWNER TO postgres;

--
-- Name: alert_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE alert_id_seq OWNED BY alert.id;


--
-- Name: download; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE download (
    id integer NOT NULL,
    report_id integer NOT NULL,
    data bytea,
    md5 text,
    sha1 text,
    sha256 text,
    size integer,
    uuid uuid,
    filename text
);


ALTER TABLE public.download OWNER TO postgres;

--
-- Name: download_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE download_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.download_id_seq OWNER TO postgres;

--
-- Name: download_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE download_id_seq OWNED BY download.id;


--
-- Name: entry; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE entry (
    id integer NOT NULL,
    report_id integer NOT NULL
);


ALTER TABLE public.entry OWNER TO postgres;

--
-- Name: entry_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE entry_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.entry_id_seq OWNER TO postgres;

--
-- Name: entry_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE entry_id_seq OWNED BY entry.id;


--
-- Name: graph; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE graph (
    id integer NOT NULL,
    report_id integer NOT NULL,
    graph bytea
);


ALTER TABLE public.graph OWNER TO postgres;

--
-- Name: graph_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE graph_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.graph_id_seq OWNER TO postgres;

--
-- Name: graph_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE graph_id_seq OWNED BY graph.id;


--
-- Name: header; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE header (
    id integer NOT NULL,
    entry_id integer,
    name text,
    value text,
    type text
);


ALTER TABLE public.header OWNER TO postgres;

--
-- Name: header_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE header_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.header_id_seq OWNER TO postgres;

--
-- Name: header_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE header_id_seq OWNED BY header.id;


--
-- Name: pcap; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE pcap (
    id integer NOT NULL,
    report_id integer,
    data bytea,
    uuid uuid
);


ALTER TABLE public.pcap OWNER TO postgres;

--
-- Name: pcap_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE pcap_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pcap_id_seq OWNER TO postgres;

--
-- Name: pcap_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE pcap_id_seq OWNED BY pcap.id;


--
-- Name: report; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE report (
    id integer NOT NULL,
    url text,
    starttime timestamp without time zone NOT NULL,
    endtime timestamp without time zone,
    uuid uuid
);


ALTER TABLE public.report OWNER TO postgres;

--
-- Name: report_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE report_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.report_id_seq OWNER TO postgres;

--
-- Name: report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE report_id_seq OWNED BY report.id;


--
-- Name: request; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE request (
    id integer NOT NULL,
    entry_id integer,
    bodysize integer,
    headersize integer,
    method text,
    uri text,
    httpversion text,
    host text,
    port integer
);


ALTER TABLE public.request OWNER TO postgres;

--
-- Name: request_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE request_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.request_id_seq OWNER TO postgres;

--
-- Name: request_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE request_id_seq OWNED BY request.id;


--
-- Name: response; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE response (
    id integer NOT NULL,
    entry_id integer,
    httpversion text,
    statustext text,
    status integer,
    bodysize integer,
    headersize integer
);


ALTER TABLE public.response OWNER TO postgres;

--
-- Name: response_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE response_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.response_id_seq OWNER TO postgres;

--
-- Name: response_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE response_id_seq OWNED BY response.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY alert ALTER COLUMN id SET DEFAULT nextval('alert_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY download ALTER COLUMN id SET DEFAULT nextval('download_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY entry ALTER COLUMN id SET DEFAULT nextval('entry_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY graph ALTER COLUMN id SET DEFAULT nextval('graph_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY header ALTER COLUMN id SET DEFAULT nextval('header_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY pcap ALTER COLUMN id SET DEFAULT nextval('pcap_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY report ALTER COLUMN id SET DEFAULT nextval('report_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY request ALTER COLUMN id SET DEFAULT nextval('request_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY response ALTER COLUMN id SET DEFAULT nextval('response_id_seq'::regclass);


--
-- Name: alert_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY alert
    ADD CONSTRAINT alert_pkey PRIMARY KEY (id);


--
-- Name: download_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY download
    ADD CONSTRAINT download_pkey PRIMARY KEY (id);


--
-- Name: entry_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY entry
    ADD CONSTRAINT entry_pkey PRIMARY KEY (id);


--
-- Name: graph_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY graph
    ADD CONSTRAINT graph_pkey PRIMARY KEY (id);


--
-- Name: header_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY header
    ADD CONSTRAINT header_pkey PRIMARY KEY (id);


--
-- Name: pcap_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY pcap
    ADD CONSTRAINT pcap_pkey PRIMARY KEY (id);


--
-- Name: report_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY report
    ADD CONSTRAINT report_pkey PRIMARY KEY (id);


--
-- Name: request_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY request
    ADD CONSTRAINT request_pkey PRIMARY KEY (id);


--
-- Name: response_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY response
    ADD CONSTRAINT response_pkey PRIMARY KEY (id);


--
-- Name: alert_report_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY alert
    ADD CONSTRAINT alert_report_id_fkey FOREIGN KEY (report_id) REFERENCES report(id);


--
-- Name: download_report_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY download
    ADD CONSTRAINT download_report_id_fkey FOREIGN KEY (report_id) REFERENCES report(id);


--
-- Name: entry_report_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY entry
    ADD CONSTRAINT entry_report_id_fkey FOREIGN KEY (report_id) REFERENCES report(id);


--
-- Name: graph_report_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY graph
    ADD CONSTRAINT graph_report_id_fkey FOREIGN KEY (report_id) REFERENCES report(id);


--
-- Name: header_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY header
    ADD CONSTRAINT header_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES entry(id);


--
-- Name: pcap_report_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY pcap
    ADD CONSTRAINT pcap_report_id_fkey FOREIGN KEY (report_id) REFERENCES report(id);


--
-- Name: request_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY request
    ADD CONSTRAINT request_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES entry(id);


--
-- Name: response_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY response
    ADD CONSTRAINT response_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES entry(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: alert; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE alert FROM PUBLIC;
REVOKE ALL ON TABLE alert FROM postgres;
GRANT ALL ON TABLE alert TO postgres;
GRANT ALL ON TABLE alert TO fjospidie;


--
-- Name: alert_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE alert_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE alert_id_seq FROM postgres;
GRANT ALL ON SEQUENCE alert_id_seq TO postgres;
GRANT ALL ON SEQUENCE alert_id_seq TO fjospidie;


--
-- Name: download; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE download FROM PUBLIC;
REVOKE ALL ON TABLE download FROM postgres;
GRANT ALL ON TABLE download TO postgres;
GRANT ALL ON TABLE download TO fjospidie;


--
-- Name: entry; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE entry FROM PUBLIC;
REVOKE ALL ON TABLE entry FROM postgres;
GRANT ALL ON TABLE entry TO postgres;
GRANT ALL ON TABLE entry TO fjospidie;


--
-- Name: entry_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE entry_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE entry_id_seq FROM postgres;
GRANT ALL ON SEQUENCE entry_id_seq TO postgres;
GRANT SELECT,USAGE ON SEQUENCE entry_id_seq TO fjospidie;


--
-- Name: graph; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE graph FROM PUBLIC;
REVOKE ALL ON TABLE graph FROM postgres;
GRANT ALL ON TABLE graph TO postgres;
GRANT ALL ON TABLE graph TO fjospidie;


--
-- Name: graph_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE graph_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE graph_id_seq FROM postgres;
GRANT ALL ON SEQUENCE graph_id_seq TO postgres;
GRANT SELECT,USAGE ON SEQUENCE graph_id_seq TO fjospidie;


--
-- Name: header; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE header FROM PUBLIC;
REVOKE ALL ON TABLE header FROM postgres;
GRANT ALL ON TABLE header TO postgres;
GRANT ALL ON TABLE header TO fjospidie;


--
-- Name: header_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE header_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE header_id_seq FROM postgres;
GRANT ALL ON SEQUENCE header_id_seq TO postgres;
GRANT SELECT,USAGE ON SEQUENCE header_id_seq TO fjospidie;


--
-- Name: pcap; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE pcap FROM PUBLIC;
REVOKE ALL ON TABLE pcap FROM postgres;
GRANT ALL ON TABLE pcap TO postgres;
GRANT ALL ON TABLE pcap TO fjospidie;


--
-- Name: pcap_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE pcap_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE pcap_id_seq FROM postgres;
GRANT ALL ON SEQUENCE pcap_id_seq TO postgres;
GRANT ALL ON SEQUENCE pcap_id_seq TO fjospidie;


--
-- Name: report; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE report FROM PUBLIC;
REVOKE ALL ON TABLE report FROM postgres;
GRANT ALL ON TABLE report TO postgres;
GRANT ALL ON TABLE report TO fjospidie;


--
-- Name: report_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE report_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE report_id_seq FROM postgres;
GRANT ALL ON SEQUENCE report_id_seq TO postgres;
GRANT SELECT,USAGE ON SEQUENCE report_id_seq TO fjospidie;


--
-- Name: request; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE request FROM PUBLIC;
REVOKE ALL ON TABLE request FROM postgres;
GRANT ALL ON TABLE request TO postgres;
GRANT ALL ON TABLE request TO fjospidie;


--
-- Name: request_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE request_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE request_id_seq FROM postgres;
GRANT ALL ON SEQUENCE request_id_seq TO postgres;
GRANT SELECT,USAGE ON SEQUENCE request_id_seq TO fjospidie;


--
-- Name: response; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE response FROM PUBLIC;
REVOKE ALL ON TABLE response FROM postgres;
GRANT ALL ON TABLE response TO postgres;
GRANT ALL ON TABLE response TO fjospidie;


--
-- Name: response_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE response_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE response_id_seq FROM postgres;
GRANT ALL ON SEQUENCE response_id_seq TO postgres;
GRANT SELECT,USAGE ON SEQUENCE response_id_seq TO fjospidie;


--
-- PostgreSQL database dump complete
--


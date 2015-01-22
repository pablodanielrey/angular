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
-- Name: account_requests; Type: TABLE; Schema: public; Owner: dcsys; Tablespace: 
--

CREATE TABLE account_requests (
    name character varying,
    lastname character varying,
    dni character varying,
    email character varying,
    reason character varying,
    id character varying
);


ALTER TABLE public.account_requests OWNER TO dcsys;

--
-- Name: password_resets; Type: TABLE; Schema: public; Owner: dcsys; Tablespace: 
--

CREATE TABLE password_resets (
    user_id character varying,
    username character varying,
    creds_id character varying,
    creation timestamp without time zone DEFAULT now(),
    hash character varying,
    executed boolean DEFAULT false
);


ALTER TABLE public.password_resets OWNER TO dcsys;

--
-- Name: user_mails; Type: TABLE; Schema: public; Owner: dcsys; Tablespace: 
--

CREATE TABLE user_mails (
    id character varying,
    user_id character varying,
    email character varying,
    confirmed boolean,
    hash character varying
);


ALTER TABLE public.user_mails OWNER TO dcsys;

--
-- Name: user_password; Type: TABLE; Schema: public; Owner: dcsys; Tablespace: 
--

CREATE TABLE user_password (
    id character varying,
    user_id character varying,
    username character varying,
    password character varying
);


ALTER TABLE public.user_password OWNER TO dcsys;

--
-- Name: users; Type: TABLE; Schema: public; Owner: dcsys; Tablespace: 
--

CREATE TABLE users (
    id character varying,
    dni character varying,
    name character varying,
    lastname character varying
);


ALTER TABLE public.users OWNER TO dcsys;

--
-- Data for Name: account_requests; Type: TABLE DATA; Schema: public; Owner: dcsys
--

COPY account_requests (name, lastname, dni, email, reason, id) FROM stdin;
\.


--
-- Data for Name: password_resets; Type: TABLE DATA; Schema: public; Owner: dcsys
--

COPY password_resets (user_id, username, creds_id, creation, hash, executed) FROM stdin;
\.


--
-- Data for Name: user_mails; Type: TABLE DATA; Schema: public; Owner: dcsys
--

COPY user_mails (id, user_id, email, confirmed, hash) FROM stdin;
2a91d6bc-995a-43e2-bcbf-6ac880d7c9cd	1c15b6b5-7594-4f9e-89c1-f94c9177ce6d	pablo@econo.unlp.edu.ar	f	
\.


--
-- Data for Name: user_password; Type: TABLE DATA; Schema: public; Owner: dcsys
--

COPY user_password (id, user_id, username, password) FROM stdin;
1	afe5c5ea-e9fa-4078-8232-c301926df65a	p	p
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: dcsys
--

COPY users (id, dni, name, lastname) FROM stdin;
1c15b6b5-7594-4f9e-89c1-f94c9177ce6d	27294557	Pablo Daniel	Rey
\.


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--


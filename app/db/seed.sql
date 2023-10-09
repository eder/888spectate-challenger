--
-- PostgreSQL database dump
--

-- Dumped from database version 12.16 (Debian 12.16-1.pgdg120+1)
-- Dumped by pg_dump version 15.3 (Debian 15.3-0+deb12u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: sportsbook_user
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO sportsbook_user;

--
-- Name: eventstatus; Type: TYPE; Schema: public; Owner: sportsbook_user
--

CREATE TYPE public.eventstatus AS ENUM (
    'pending',
    'started',
    'ended',
    'cancelled'
);


ALTER TYPE public.eventstatus OWNER TO sportsbook_user;

--
-- Name: eventtype; Type: TYPE; Schema: public; Owner: sportsbook_user
--

CREATE TYPE public.eventtype AS ENUM (
    'preplay',
    'inplay'
);


ALTER TYPE public.eventtype OWNER TO sportsbook_user;

--
-- Name: selectionoutcome; Type: TYPE; Schema: public; Owner: sportsbook_user
--

CREATE TYPE public.selectionoutcome AS ENUM (
    'unsettled',
    'void',
    'lose',
    'win'
);


ALTER TYPE public.selectionoutcome OWNER TO sportsbook_user;

--
-- Name: generate_slug(text); Type: FUNCTION; Schema: public; Owner: sportsbook_user
--

CREATE FUNCTION public.generate_slug(p_input text) RETURNS text
    LANGUAGE plpgsql
    AS $$
BEGIN
  RETURN LOWER(REPLACE(p_input, ' ', '-'));
END;
$$;


ALTER FUNCTION public.generate_slug(p_input text) OWNER TO sportsbook_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: sportsbook_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO sportsbook_user;

--
-- Name: events; Type: TABLE; Schema: public; Owner: sportsbook_user
--

CREATE TABLE public.events (
    id integer NOT NULL,
    name character varying NOT NULL,
    slug character varying NOT NULL,
    active boolean,
    type public.eventtype NOT NULL,
    sport_id integer NOT NULL,
    status public.eventstatus NOT NULL,
    scheduled_start timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    actual_start timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.events OWNER TO sportsbook_user;

--
-- Name: events_id_seq; Type: SEQUENCE; Schema: public; Owner: sportsbook_user
--

CREATE SEQUENCE public.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_id_seq OWNER TO sportsbook_user;

--
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sportsbook_user
--

ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;


--
-- Name: selections; Type: TABLE; Schema: public; Owner: sportsbook_user
--

CREATE TABLE public.selections (
    id integer NOT NULL,
    name character varying NOT NULL,
    event_id integer NOT NULL,
    price double precision NOT NULL,
    active boolean,
    outcome public.selectionoutcome NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.selections OWNER TO sportsbook_user;

--
-- Name: selections_id_seq; Type: SEQUENCE; Schema: public; Owner: sportsbook_user
--

CREATE SEQUENCE public.selections_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.selections_id_seq OWNER TO sportsbook_user;

--
-- Name: selections_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sportsbook_user
--

ALTER SEQUENCE public.selections_id_seq OWNED BY public.selections.id;


--
-- Name: sports; Type: TABLE; Schema: public; Owner: sportsbook_user
--

CREATE TABLE public.sports (
    id integer NOT NULL,
    name character varying NOT NULL,
    slug character varying NOT NULL,
    active boolean,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.sports OWNER TO sportsbook_user;

--
-- Name: sports_id_seq; Type: SEQUENCE; Schema: public; Owner: sportsbook_user
--

CREATE SEQUENCE public.sports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sports_id_seq OWNER TO sportsbook_user;

--
-- Name: sports_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sportsbook_user
--

ALTER SEQUENCE public.sports_id_seq OWNED BY public.sports.id;


--
-- Name: events id; Type: DEFAULT; Schema: public; Owner: sportsbook_user
--

ALTER TABLE ONLY public.events ALTER COLUMN id SET DEFAULT nextval('public.events_id_seq'::regclass);


--
-- Name: selections id; Type: DEFAULT; Schema: public; Owner: sportsbook_user
--

ALTER TABLE ONLY public.selections ALTER COLUMN id SET DEFAULT nextval('public.selections_id_seq'::regclass);


--
-- Name: sports id; Type: DEFAULT; Schema: public; Owner: sportsbook_user
--

ALTER TABLE ONLY public.sports ALTER COLUMN id SET DEFAULT nextval('public.sports_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: sportsbook_user
--

COPY public.alembic_version (version_num) FROM stdin;
1696377583
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: sportsbook_user
--

COPY public.events (id, name, slug, active, type, sport_id, status, scheduled_start, actual_start, created_at, updated_at) FROM stdin;
39	Match TeamA vs TeamB	match-teama-vs-teamb	t	inplay	24	started	2023-10-08 12:58:53.870038+00	2023-10-08 12:58:53.870038+00	2023-10-08 12:58:53.870038+00	2023-10-08 12:58:53.870038+00
40	Match TeamC vs TeamD	match-teamc-vs-teamd	t	inplay	24	started	2023-10-08 12:58:53.877239+00	2023-10-08 12:58:53.877239+00	2023-10-08 12:58:53.877239+00	2023-10-08 12:58:53.877239+00
41	Game TeamE vs TeamF	game-teame-vs-teamf	t	inplay	25	started	2023-10-08 12:58:53.878694+00	2023-10-08 12:58:53.878694+00	2023-10-08 12:58:53.878694+00	2023-10-08 12:58:53.878694+00
42	Game TeamG vs TeamH	game-teamg-vs-teamh	f	inplay	25	started	2023-10-08 12:58:53.879831+00	2023-10-08 12:58:53.879831+00	2023-10-08 12:58:53.879831+00	2023-10-08 12:58:53.879831+00
43	Game TeamI vs TeamJ	game-teami-vs-teamj	t	inplay	25	started	2023-10-08 12:58:53.885272+00	2023-10-08 12:58:53.885272+00	2023-10-08 12:58:53.885272+00	2023-10-08 12:58:53.885272+00
44	Match PlayerK vs PlayerL	match-playerk-vs-playerl	f	inplay	26	started	2023-10-08 12:58:53.887608+00	2023-10-08 12:58:53.887608+00	2023-10-08 12:58:53.887608+00	2023-10-08 12:58:53.887608+00
\.


--
-- Data for Name: selections; Type: TABLE DATA; Schema: public; Owner: sportsbook_user
--

COPY public.selections (id, name, event_id, price, active, outcome, created_at, updated_at) FROM stdin;
26	TeamA Win	39	1.5	t	win	2023-10-08 13:00:31.913678+00	2023-10-08 13:00:31.913678+00
\.


--
-- Data for Name: sports; Type: TABLE DATA; Schema: public; Owner: sportsbook_user
--

COPY public.sports (id, name, slug, active, created_at, updated_at) FROM stdin;
24	Football	football	t	2023-10-08 12:55:52.947355+00	2023-10-08 12:55:52.947355+00
25	Basketball	basketball	t	2023-10-08 12:55:52.95697+00	2023-10-08 12:55:52.95697+00
26	Tennis	tennis	t	2023-10-08 12:55:52.96094+00	2023-10-08 12:55:52.96094+00
27	Boxing	boxing	t	2023-10-08 18:24:11.724542+00	2023-10-08 18:24:11.724542+00
\.


--
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sportsbook_user
--

SELECT pg_catalog.setval('public.events_id_seq', 44, true);


--
-- Name: selections_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sportsbook_user
--

SELECT pg_catalog.setval('public.selections_id_seq', 26, true);


--
-- Name: sports_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sportsbook_user
--

SELECT pg_catalog.setval('public.sports_id_seq', 27, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: sportsbook_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: sportsbook_user
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- Name: events events_slug_key; Type: CONSTRAINT; Schema: public; Owner: sportsbook_user
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_slug_key UNIQUE (slug);


--
-- Name: selections selections_pkey; Type: CONSTRAINT; Schema: public; Owner: sportsbook_user
--

ALTER TABLE ONLY public.selections
    ADD CONSTRAINT selections_pkey PRIMARY KEY (id);


--
-- Name: sports sports_pkey; Type: CONSTRAINT; Schema: public; Owner: sportsbook_user
--

ALTER TABLE ONLY public.sports
    ADD CONSTRAINT sports_pkey PRIMARY KEY (id);


--
-- Name: sports sports_slug_key; Type: CONSTRAINT; Schema: public; Owner: sportsbook_user
--

ALTER TABLE ONLY public.sports
    ADD CONSTRAINT sports_slug_key UNIQUE (slug);


--
-- Name: events events_sport_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sportsbook_user
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_sport_id_fkey FOREIGN KEY (sport_id) REFERENCES public.sports(id);


--
-- Name: selections selections_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sportsbook_user
--

ALTER TABLE ONLY public.selections
    ADD CONSTRAINT selections_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: sportsbook_user
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--


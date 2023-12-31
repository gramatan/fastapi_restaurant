--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1
-- Dumped by pg_dump version 15.2

-- Started on 2023-08-12 14:00:28

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 219 (class 1259 OID 16620)
-- Name: dishes; Type: TABLE; Schema: public; Owner: ylab
--

CREATE TABLE public.dishes (
    id integer NOT NULL,
    manual_id character varying,
    title character varying,
    description character varying,
    price numeric(10,2),
    submenu_id integer
);


ALTER TABLE public.dishes OWNER TO ylab;

--
-- TOC entry 218 (class 1259 OID 16619)
-- Name: dishes_id_seq; Type: SEQUENCE; Schema: public; Owner: ylab
--

CREATE SEQUENCE public.dishes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dishes_id_seq OWNER TO ylab;

--
-- TOC entry 3386 (class 0 OID 0)
-- Dependencies: 218
-- Name: dishes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ylab
--

ALTER SEQUENCE public.dishes_id_seq OWNED BY public.dishes.id;


--
-- TOC entry 215 (class 1259 OID 16587)
-- Name: menus; Type: TABLE; Schema: public; Owner: ylab
--

CREATE TABLE public.menus (
    id integer NOT NULL,
    manual_id character varying,
    title character varying,
    description character varying
);


ALTER TABLE public.menus OWNER TO ylab;

--
-- TOC entry 214 (class 1259 OID 16586)
-- Name: menus_id_seq; Type: SEQUENCE; Schema: public; Owner: ylab
--

CREATE SEQUENCE public.menus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.menus_id_seq OWNER TO ylab;

--
-- TOC entry 3387 (class 0 OID 0)
-- Dependencies: 214
-- Name: menus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ylab
--

ALTER SEQUENCE public.menus_id_seq OWNED BY public.menus.id;


--
-- TOC entry 217 (class 1259 OID 16601)
-- Name: submenus; Type: TABLE; Schema: public; Owner: ylab
--

CREATE TABLE public.submenus (
    id integer NOT NULL,
    manual_id character varying,
    title character varying,
    description character varying,
    menu_id integer
);


ALTER TABLE public.submenus OWNER TO ylab;

--
-- TOC entry 216 (class 1259 OID 16600)
-- Name: submenus_id_seq; Type: SEQUENCE; Schema: public; Owner: ylab
--

CREATE SEQUENCE public.submenus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.submenus_id_seq OWNER TO ylab;

--
-- TOC entry 3388 (class 0 OID 0)
-- Dependencies: 216
-- Name: submenus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ylab
--

ALTER SEQUENCE public.submenus_id_seq OWNED BY public.submenus.id;


--
-- TOC entry 3208 (class 2604 OID 16623)
-- Name: dishes id; Type: DEFAULT; Schema: public; Owner: ylab
--

ALTER TABLE ONLY public.dishes ALTER COLUMN id SET DEFAULT nextval('public.dishes_id_seq'::regclass);


--
-- TOC entry 3206 (class 2604 OID 16590)
-- Name: menus id; Type: DEFAULT; Schema: public; Owner: ylab
--

ALTER TABLE ONLY public.menus ALTER COLUMN id SET DEFAULT nextval('public.menus_id_seq'::regclass);


--
-- TOC entry 3207 (class 2604 OID 16604)
-- Name: submenus id; Type: DEFAULT; Schema: public; Owner: ylab
--

ALTER TABLE ONLY public.submenus ALTER COLUMN id SET DEFAULT nextval('public.submenus_id_seq'::regclass);


--
-- TOC entry 3380 (class 0 OID 16620)
-- Dependencies: 219
-- Data for Name: dishes; Type: TABLE DATA; Schema: public; Owner: ylab
--

COPY public.dishes (id, manual_id, title, description, price, submenu_id) FROM stdin;
\.


--
-- TOC entry 3376 (class 0 OID 16587)
-- Dependencies: 215
-- Data for Name: menus; Type: TABLE DATA; Schema: public; Owner: ylab
--

COPY public.menus (id, manual_id, title, description) FROM stdin;
\.


--
-- TOC entry 3378 (class 0 OID 16601)
-- Dependencies: 217
-- Data for Name: submenus; Type: TABLE DATA; Schema: public; Owner: ylab
--

COPY public.submenus (id, manual_id, title, description, menu_id) FROM stdin;
\.


--
-- TOC entry 3389 (class 0 OID 0)
-- Dependencies: 218
-- Name: dishes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ylab
--

SELECT pg_catalog.setval('public.dishes_id_seq', 1, false);


--
-- TOC entry 3390 (class 0 OID 0)
-- Dependencies: 214
-- Name: menus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ylab
--

SELECT pg_catalog.setval('public.menus_id_seq', 1, false);


--
-- TOC entry 3391 (class 0 OID 0)
-- Dependencies: 216
-- Name: submenus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ylab
--

SELECT pg_catalog.setval('public.submenus_id_seq', 1, false);


--
-- TOC entry 3224 (class 2606 OID 16629)
-- Name: dishes dishes_manual_id_key; Type: CONSTRAINT; Schema: public; Owner: ylab
--

ALTER TABLE ONLY public.dishes
    ADD CONSTRAINT dishes_manual_id_key UNIQUE (manual_id);


--
-- TOC entry 3226 (class 2606 OID 16627)
-- Name: dishes dishes_pkey; Type: CONSTRAINT; Schema: public; Owner: ylab
--

ALTER TABLE ONLY public.dishes
    ADD CONSTRAINT dishes_pkey PRIMARY KEY (id);


--
-- TOC entry 3213 (class 2606 OID 16596)
-- Name: menus menus_manual_id_key; Type: CONSTRAINT; Schema: public; Owner: ylab
--

ALTER TABLE ONLY public.menus
    ADD CONSTRAINT menus_manual_id_key UNIQUE (manual_id);


--
-- TOC entry 3215 (class 2606 OID 16594)
-- Name: menus menus_pkey; Type: CONSTRAINT; Schema: public; Owner: ylab
--

ALTER TABLE ONLY public.menus
    ADD CONSTRAINT menus_pkey PRIMARY KEY (id);


--
-- TOC entry 3220 (class 2606 OID 16610)
-- Name: submenus submenus_manual_id_key; Type: CONSTRAINT; Schema: public; Owner: ylab
--

ALTER TABLE ONLY public.submenus
    ADD CONSTRAINT submenus_manual_id_key UNIQUE (manual_id);


--
-- TOC entry 3222 (class 2606 OID 16608)
-- Name: submenus submenus_pkey; Type: CONSTRAINT; Schema: public; Owner: ylab
--

ALTER TABLE ONLY public.submenus
    ADD CONSTRAINT submenus_pkey PRIMARY KEY (id);


--
-- TOC entry 3227 (class 1259 OID 16638)
-- Name: ix_dishes_description; Type: INDEX; Schema: public; Owner: ylab
--

CREATE INDEX ix_dishes_description ON public.dishes USING btree (description);


--
-- TOC entry 3228 (class 1259 OID 16637)
-- Name: ix_dishes_id; Type: INDEX; Schema: public; Owner: ylab
--

CREATE INDEX ix_dishes_id ON public.dishes USING btree (id);


--
-- TOC entry 3229 (class 1259 OID 16636)
-- Name: ix_dishes_price; Type: INDEX; Schema: public; Owner: ylab
--

CREATE INDEX ix_dishes_price ON public.dishes USING btree (price);


--
-- TOC entry 3230 (class 1259 OID 16635)
-- Name: ix_dishes_title; Type: INDEX; Schema: public; Owner: ylab
--

CREATE INDEX ix_dishes_title ON public.dishes USING btree (title);


--
-- TOC entry 3209 (class 1259 OID 16597)
-- Name: ix_menus_description; Type: INDEX; Schema: public; Owner: ylab
--

CREATE INDEX ix_menus_description ON public.menus USING btree (description);


--
-- TOC entry 3210 (class 1259 OID 16598)
-- Name: ix_menus_id; Type: INDEX; Schema: public; Owner: ylab
--

CREATE INDEX ix_menus_id ON public.menus USING btree (id);


--
-- TOC entry 3211 (class 1259 OID 16599)
-- Name: ix_menus_title; Type: INDEX; Schema: public; Owner: ylab
--

CREATE INDEX ix_menus_title ON public.menus USING btree (title);


--
-- TOC entry 3216 (class 1259 OID 16617)
-- Name: ix_submenus_description; Type: INDEX; Schema: public; Owner: ylab
--

CREATE INDEX ix_submenus_description ON public.submenus USING btree (description);


--
-- TOC entry 3217 (class 1259 OID 16618)
-- Name: ix_submenus_id; Type: INDEX; Schema: public; Owner: ylab
--

CREATE INDEX ix_submenus_id ON public.submenus USING btree (id);


--
-- TOC entry 3218 (class 1259 OID 16616)
-- Name: ix_submenus_title; Type: INDEX; Schema: public; Owner: ylab
--

CREATE INDEX ix_submenus_title ON public.submenus USING btree (title);


--
-- TOC entry 3232 (class 2606 OID 16630)
-- Name: dishes dishes_submenu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ylab
--

ALTER TABLE ONLY public.dishes
    ADD CONSTRAINT dishes_submenu_id_fkey FOREIGN KEY (submenu_id) REFERENCES public.submenus(id) ON DELETE CASCADE;


--
-- TOC entry 3231 (class 2606 OID 16611)
-- Name: submenus submenus_menu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ylab
--

ALTER TABLE ONLY public.submenus
    ADD CONSTRAINT submenus_menu_id_fkey FOREIGN KEY (menu_id) REFERENCES public.menus(id) ON DELETE CASCADE;


-- Completed on 2023-08-12 14:00:29

--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.4.26
-- Dumped by pg_dump version 11.17 (Debian 11.17-0+deb10u1)

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
-- Name: sirest; Type: SCHEMA; Schema: -; Owner: db22b006
--

CREATE SCHEMA sirest;


ALTER SCHEMA sirest OWNER TO db22b006;

--
-- Name: cek_tgl_promo_valid(); Type: FUNCTION; Schema: sirest; Owner: db22b006
--

CREATE FUNCTION sirest.cek_tgl_promo_valid() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    DECLARE
        cek_tgl date;
        start_date date;
        end_date date;
    BEGIN
        IF(TG_OP = 'INSERT') THEN
            SELECT NEW.Datetime into cek_tgl
            FROM SPECIAL_DAY_PROMO JOIN RESTAURANT_PROMO RP ON RP.PId = Id;
            SELECT Start::date into start_date
            FROM RESTAURANT_PROMO JOIN SPECIAL_DAY_PROMO SDP ON PId = SDP.Id;
            SELECT "end"::date into end_date
            FROM RESTAURANT_PROMO JOIN SPECIAL_DAY_PROMO SDP ON PId = SDP.Id;
            IF(cek_tgl < start_date) THEN
                RAISE EXCEPTION 'Promo tidak valid';
            ELSEIF(cek_tgl > end_date) THEN
                RAISE EXCEPTION 'Promo tidak valid';
            END IF;
            RETURN NEW;
        END IF;
	END;
$$;


ALTER FUNCTION sirest.cek_tgl_promo_valid() OWNER TO db22b006;

--
-- Name: cekbiayapengantaran(); Type: FUNCTION; Schema: sirest; Owner: db22b006
--

CREATE FUNCTION sirest.cekbiayapengantaran() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    DECLARE
        biaya_pengantaran INTEGER;
    BEGIN       
        IF (NEW.vehicletype = 'Mobil') THEN
            SELECT carfee INTO biaya_pengantaran
            FROM delivery_fee_per_km dfpk
            WHERE dfpk.id = NEW.dfid;
        ELSE
            SELECT motorfee INTO biaya_pengantaran
            FROM delivery_fee_per_km dfpk
            WHERE dfpk.id = NEW.dfid;
        END IF;

        NEW.deliveryfee := biaya_pengantaran * 2;
        new.totalPrice := new.totalFood + new.deliveryfee - new.totaldiscount;
        RETURN NEW;
    END;
$$;


ALTER FUNCTION sirest.cekbiayapengantaran() OWNER TO db22b006;

--
-- Name: check_password(); Type: FUNCTION; Schema: sirest; Owner: db22b006
--

CREATE FUNCTION sirest.check_password() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.password NOT SIMILAR TO '%\d+%' THEN
        RAISE EXCEPTION 'Password must contains minimal one number';
    END IF;
    IF NEW.password NOT SIMILAR TO 
    '%[A-Z]%' THEN RAISE EXCEPTION 'Password must contains minimal
    one capital letters';
    END IF ;
    RETURN NEW;
END;
$$;


ALTER FUNCTION sirest.check_password() OWNER TO db22b006;

--
-- Name: checkbalance(); Type: FUNCTION; Schema: sirest; Owner: db22b006
--

CREATE FUNCTION sirest.checkbalance() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
	current_balance INT;
BEGIN
	IF(TG_OP='UPDATE')THEN
		SELECT RestoPay INTO current_balance
		FROM TRANSACTION_ACTOR WHERE Email = new.Email;
		
		IF (new.RestoPay < 0) THEN
			IF (new.Restopay * -1 > current_balance) THEN
				RAISE EXCEPTION 'Jumlah saldo tidak mencukupi.';
			END IF;
		END IF;
		NEW.restopay = current_balance + NEW.restopay;
		RETURN NEW;
	END IF;
END
$$;


ALTER FUNCTION sirest.checkbalance() OWNER TO db22b006;

--
-- Name: checktarif(); Type: FUNCTION; Schema: sirest; Owner: db22b006
--

CREATE FUNCTION sirest.checktarif() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	IF (NEW.motorfee >= NEW.carfee) THEN
		RAISE EXCEPTION 'Tarif mobil harus lebih besar dari motor';
	END IF;
	IF (NEW.motorfee > 7000 OR NEW.motorfee < 2000 OR NEW.carfee > 7000 OR NEW.carfee < 2000) THEN 
	RAISE EXCEPTION 'Tarif tidak sesuai dengan aturan';
	END IF;
END;
$$;


ALTER FUNCTION sirest.checktarif() OWNER TO db22b006;

--
-- Name: update_restopay(); Type: FUNCTION; Schema: sirest; Owner: db22b006
--

CREATE FUNCTION sirest.update_restopay() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    new_restopay_courier integer;
    new_restopay_resto integer;
BEGIN
    IF (NEW.name = 'Completed Order') THEN
        SELECT restopay INTO new_restopay_resto FROM restaurant r, transaction_status ts, transaction_actor ta, transaction_history th WHERE r.email = ta.email AND th.tsid = ts.id AND ts.name = 'Completed Order' AND th.tsid = NEW.ID; 
        SELECT restopay INTO new_restopay_courier FROM courier c, transaction_actor ta, transaction_status ts, transaction_history th WHERE c.email = ta.email AND th.tsid = ts.id AND ts.name = 'Completed Order' AND th.tsid = NEW.ID;
        new_restopay_resto = new_restopay_resto + NEW.totalprice;
        new_restopay_courier = new_restopay_courier + NEW.deliveryfee;
        UPDATE transaction_actor SET restopay = new_restopay_resto WHERE email = r.email;
        UPDATE transaction_actor SET restopay = new_restopay_courier WHERE email = c.email;
    END IF;
    RETURN NEW;
END;
$$;


ALTER FUNCTION sirest.update_restopay() OWNER TO db22b006;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: admin; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.admin (
    email character varying(50) NOT NULL
);


ALTER TABLE sirest.admin OWNER TO db22b006;

--
-- Name: courier; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.courier (
    email character varying(50) NOT NULL,
    platenum character varying(10) NOT NULL,
    drivinglicensenum character varying(20) NOT NULL,
    vehicletype character varying(15) NOT NULL,
    vehiclebrand character varying(15) NOT NULL
);


ALTER TABLE sirest.courier OWNER TO db22b006;

--
-- Name: customer; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.customer (
    email character varying(50) NOT NULL,
    birthdate date NOT NULL,
    sex character(1) NOT NULL
);


ALTER TABLE sirest.customer OWNER TO db22b006;

--
-- Name: delivery_fee_per_km; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.delivery_fee_per_km (
    id character varying(20) NOT NULL,
    province character varying(25) NOT NULL,
    motorfee integer NOT NULL,
    carfee integer NOT NULL
);


ALTER TABLE sirest.delivery_fee_per_km OWNER TO db22b006;

--
-- Name: food; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.food (
    rname character varying(25) NOT NULL,
    rbranch character varying(25) NOT NULL,
    foodname character varying(50) NOT NULL,
    description text,
    stock integer NOT NULL,
    price bigint NOT NULL,
    fcategory character varying(20) NOT NULL
);


ALTER TABLE sirest.food OWNER TO db22b006;

--
-- Name: food_category; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.food_category (
    id character varying(20) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE sirest.food_category OWNER TO db22b006;

--
-- Name: food_ingredients; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.food_ingredients (
    rname character varying(25) NOT NULL,
    rbranch character varying(25) NOT NULL,
    foodname character varying(50) NOT NULL,
    ingredient character varying(25)
);


ALTER TABLE sirest.food_ingredients OWNER TO db22b006;

--
-- Name: ingredient; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.ingredient (
    id character varying(25) NOT NULL,
    name character varying(25) NOT NULL
);


ALTER TABLE sirest.ingredient OWNER TO db22b006;

--
-- Name: min_transaction_promo; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.min_transaction_promo (
    id character varying(25) NOT NULL,
    minimumtransactionnum integer NOT NULL
);


ALTER TABLE sirest.min_transaction_promo OWNER TO db22b006;

--
-- Name: payment_method; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.payment_method (
    id character varying(25) NOT NULL,
    name character varying(25) NOT NULL
);


ALTER TABLE sirest.payment_method OWNER TO db22b006;

--
-- Name: payment_status; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.payment_status (
    id character varying(25) NOT NULL,
    name character varying(25) NOT NULL
);


ALTER TABLE sirest.payment_status OWNER TO db22b006;

--
-- Name: promo; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.promo (
    id character varying(25) NOT NULL,
    promoname character varying(25) NOT NULL,
    discount integer NOT NULL,
    CONSTRAINT promo_discount_check CHECK ((1 <= discount)),
    CONSTRAINT promo_discount_check1 CHECK ((discount <= 100))
);


ALTER TABLE sirest.promo OWNER TO db22b006;

--
-- Name: restaurant; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.restaurant (
    rname character varying(25) NOT NULL,
    rbranch character varying(25) NOT NULL,
    email character varying(50) NOT NULL,
    rphonenum character varying(18) NOT NULL,
    street character varying(30) NOT NULL,
    district character varying(20) NOT NULL,
    city character varying(20) NOT NULL,
    province character varying(20) NOT NULL,
    rating integer DEFAULT 0 NOT NULL,
    rcategory character varying(20) NOT NULL
);


ALTER TABLE sirest.restaurant OWNER TO db22b006;

--
-- Name: restaurant_category; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.restaurant_category (
    id character varying(20) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE sirest.restaurant_category OWNER TO db22b006;

--
-- Name: restaurant_operating_hours; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.restaurant_operating_hours (
    name character varying(25) NOT NULL,
    branch character varying(25) NOT NULL,
    day character varying(10) NOT NULL,
    starthours time without time zone NOT NULL,
    endhours time without time zone NOT NULL
);


ALTER TABLE sirest.restaurant_operating_hours OWNER TO db22b006;

--
-- Name: restaurant_promo; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.restaurant_promo (
    rname character varying(25) NOT NULL,
    rbranch character varying(25) NOT NULL,
    pid character varying(25) NOT NULL,
    start timestamp without time zone NOT NULL,
    "end" timestamp without time zone NOT NULL
);


ALTER TABLE sirest.restaurant_promo OWNER TO db22b006;

--
-- Name: special_day_promo; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.special_day_promo (
    id character varying(25) NOT NULL,
    datetime date NOT NULL
);


ALTER TABLE sirest.special_day_promo OWNER TO db22b006;

--
-- Name: temp; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.temp (
    rname character varying(25) NOT NULL,
    rbranch character varying(25) NOT NULL,
    foodname character varying(50) NOT NULL,
    pid character varying(25) NOT NULL,
    start timestamp without time zone NOT NULL,
    "end" timestamp without time zone NOT NULL
);


ALTER TABLE sirest.temp OWNER TO db22b006;

--
-- Name: transaction; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.transaction (
    email character varying(50) NOT NULL,
    datetime timestamp without time zone NOT NULL,
    street character varying(30) NOT NULL,
    district character varying(30) NOT NULL,
    city character varying(25) NOT NULL,
    province character varying(25) NOT NULL,
    totalfood double precision NOT NULL,
    totaldiscount double precision NOT NULL,
    deliveryfee double precision NOT NULL,
    totalprice double precision NOT NULL,
    rating integer,
    pmid character varying(25) NOT NULL,
    psid character varying(25) NOT NULL,
    dfid character varying(20) NOT NULL,
    courierid character varying(50),
    vehicletype character varying(15) DEFAULT 'Mobil'::character varying NOT NULL
);


ALTER TABLE sirest.transaction OWNER TO db22b006;

--
-- Name: transaction_actor; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.transaction_actor (
    email character varying(50) NOT NULL,
    nik character varying(20) NOT NULL,
    bankname character varying(20) NOT NULL,
    accountno character varying(20) NOT NULL,
    restopay bigint DEFAULT 0 NOT NULL,
    adminid character varying(50)
);


ALTER TABLE sirest.transaction_actor OWNER TO db22b006;

--
-- Name: transaction_food; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.transaction_food (
    email character varying(50) NOT NULL,
    datetime timestamp without time zone NOT NULL,
    rname character varying(50) NOT NULL,
    rbranch character varying(25) NOT NULL,
    foodname character varying(50) NOT NULL,
    amount integer NOT NULL,
    note character varying(255)
);


ALTER TABLE sirest.transaction_food OWNER TO db22b006;

--
-- Name: transaction_history; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.transaction_history (
    email character varying(50) NOT NULL,
    datetime timestamp without time zone NOT NULL,
    tsid character varying(25) NOT NULL,
    datetimestatus timestamp without time zone NOT NULL
);


ALTER TABLE sirest.transaction_history OWNER TO db22b006;

--
-- Name: transaction_status; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.transaction_status (
    id character varying(25) NOT NULL,
    name character varying(25) NOT NULL
);


ALTER TABLE sirest.transaction_status OWNER TO db22b006;

--
-- Name: user_acc; Type: TABLE; Schema: sirest; Owner: db22b006
--

CREATE TABLE sirest.user_acc (
    email character varying(50) NOT NULL,
    password character varying(50) NOT NULL,
    phonenum character varying(20) NOT NULL,
    fname character varying(15) NOT NULL,
    lname character varying(15) NOT NULL
);


ALTER TABLE sirest.user_acc OWNER TO db22b006;

--
-- Data for Name: admin; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.admin (email) FROM stdin;
rhuskinson0@opensource.org
cmcileen1@usda.gov
abachman2@yahoo.co.jp
lashbolt3@tamu.edu
psiegertsz4@zdnet.com
\.


--
-- Data for Name: courier; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.courier (email, platenum, drivinglicensenum, vehicletype, vehiclebrand) FROM stdin;
mboyatm@feedburner.com	8469	983373318180	Motor	Honda
sbraunfeldi@weebly.com	8304	264734761335	Mobil	Hyundai
gstaddartr@reference.com	6996	200592933677	Motor	Hyundai
nwinckwortho@imageshack.us	3920	907492562189	Mobil	Honda
cglasbeyk@foxnews.com	6657	385606502797	Mobil	BMW
spritchett5@earthlink.net	1234	467773402599	Motor	Yamaha
tbranchet6@google.co.jp	5643	585101512390	Mobil	Suzuki
rheinreich7@liveinternet.ru	9098	678906112337	Motor	Yamaha
kgosdin9@aboutads.info	9055	356789522107	Motor	Honda
lhandrekt@google.co.jp	6521	687676703732	Mobil	Hyundai
\.


--
-- Data for Name: customer; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.customer (email, birthdate, sex) FROM stdin;
arapkins8@reddit.com	1998-01-28	F
pcumeskya@columbia.edu	2000-05-16	F
rhyndn@posterous.com	2000-10-05	M
lgeekinp@bandcamp.com	2001-11-23	F
sfritchlyl@dailymail.co.uk	2001-10-20	F
bpimbleyq@hhs.gov	2000-03-28	M
baitchisonj@newyorker.com	2001-04-10	M
htufts@hubpages.com	1999-12-04	F
bmacalpyneh@mac.com	2000-12-15	F
akobierag@cmu.edu	1997-08-23	M
bsturgeonf@tuttocitta.it	1999-10-01	F
hsimcoe@vimeo.com	1998-10-20	M
mgallgherd@unblog.fr	1999-03-03	M
rmoncrefeb@businesswire.com	2001-07-12	M
dkroonc@google.com.au	1999-08-19	M
ewycliffe1@dropbox.com	2001-02-27	F
dmasurel0@etsy.com	1999-10-08	F
bbarkly2@si.edu	2000-09-02	F
nbreward3@walmart.com	2000-05-19	F
dpetrie4@twitpic.com	2000-05-09	F
\.


--
-- Data for Name: delivery_fee_per_km; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.delivery_fee_per_km (id, province, motorfee, carfee) FROM stdin;
x9LN21jUNb	Virginia	12	24
MrNHF5fUhz	New York	15	25
rbIbekPXfq	California	15	30
VAxb5ptyYr	Texas	14	22
57L0H5CX68	Michigan	10	21
L4Jj5kHCW4	Utah	14	29
JoHV435OwO	Maryland	15	22
FMXOzFTJC2	Mississippi	13	26
HVsrVpnAMC	Pennsylvania	18	28
EimwxrdNbn	Arkansas	10	20
\.


--
-- Data for Name: food; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.food (rname, rbranch, foodname, description, stock, price, fcategory) FROM stdin;
Skynoodle	Glyburide	 Form	Hurricane, subsequent encounter	100	305837	70520393-c512
Skynoodle	Glyburide	Uniform Whiskey Lima	Other fracture of occiput, right side, init	64	153700	70520393-c512
Skynoodle	Glyburide	 Hotel	Other water transport accident	73	554985	2c8cfc88-530f
Skynoodle	Glyburide	Yankee Romeo Uniform Hotel 	Type 2 diabetes mellitus with other skin ulcer	97	290207	2c8cfc88-530f
Yacero	THE	 Uniform Hotel Lima 	Poisoning by thrombolytic drug, intentional self-harm, subs	35	509299	06f80b2c-bda6
Yacero	THE	LimaRomeo	Partial traumatic MCP amputation of right middle finger	15	110810	70520393-c512
Yacero	THE	Romeo Hotel Lima	Shock due to anesthesia, subsequent encounter	59	117992	06f80b2c-bda6
Yacero	THE	 Hotel Uniform 	Unspecified asthma	6	210358	2c8cfc88-530f
Trudoo	Lamotrigine	 Lima 	Legal intervnt w injury by explosv shell, bystand inj, subs	52	610569	70520393-c512
Trudoo	Lamotrigine	 Uniform Lima Sierra Hotel	Oth secondary chronic gout, right ankle and foot, w tophus	57	375911	69a47987-d54b
Trudoo	Lamotrigine	Yankee Charlie UniformHotel 	Sickle-cell thalassemia with crisis, unspecified	58	684807	70520393-c512
Trudoo	Lamotrigine	 Hotel LimaRomeo	Injury due to collapse of burning bldg in ctrl fire, subs	61	32617	69a47987-d54b
Meevee	Levaquin	 Charlie YankeeLima Romeo 	Adolescent idiopathic scoliosis, site unspecified	13	93021	69a47987-d54b
Meevee	Levaquin	LimaUniform Hotel	Complications of reattached (part of) unsp lower extremity	56	68209	69a47987-d54b
Meevee	Levaquin	 UniformRomeoYankee 	Unsp nondisp fx of first cervical vertebra, init for opn fx	96	239934	70520393-c512
Meevee	Levaquin	 LimaCharlieYankeeRomeoSierraUniform	Assault by sharp glass, sequela	39	592737	69a47987-d54b
Yoveo	Levofloxacin	 Lima Sierra 	Nondisp fx of olecran pro w intartic extn r ulna, 7thH	99	344655	70520393-c512
Yoveo	Levofloxacin	 Lima UniformHotel	Foreign body in nostril, subsequent encounter	86	98276	8a230bfe-c6c6
Yoveo	Levofloxacin	 Romeo WhiskeyCharlie 	Displaced transverse fracture of shaft of unsp ulna, init	32	731609	8a230bfe-c6c6
Yoveo	Levofloxacin	 Yankee Lima Romeo	Nondisp segmental fracture of shaft of right fibula, init	12	328833	69a47987-d54b
Feednation	DEXTROSE	HotelUniform SierraRomeo 	Filamentary keratitis, left eye	51	594545	8a230bfe-c6c6
Feednation	DEXTROSE	Uniform Lima HotelRomeo	Echinococcus multilocularis infct, oth and multiple sites	34	13143	06f80b2c-bda6
Feednation	DEXTROSE	HotelCharlieUniform	Mtrcy driver injured in clsn w rail trn/veh in traf, subs	78	458735	2c8cfc88-530f
Feednation	DEXTROSE	 Romeo 	Poisn by oth antieplptc and sed-hypntc drugs, asslt, sequela	55	451139	06f80b2c-bda6
Tagopia	Headache	HotelLimaSierraYankee	Toxic effect of contact w Portugese Man-o-war, undet, subs	67	241581	8a230bfe-c6c6
Tagopia	Headache	 Romeo Hotel Uniform	Lac w/o fb of unsp external genital organs, male, sequela	96	210187	69a47987-d54b
Tagopia	Headache	 Hotel RomeoLimaUniformCharlie	Lacerat long flexor musc/fasc/tend right thumb at wrs/hnd lv	41	658452	69a47987-d54b
Tagopia	Headache	HotelYankee Uniform	Unsp pedl cyclst injured in clsn w unsp mv nontraf, init	53	720750	8a230bfe-c6c6
Mycat	Lovastatin	Uniform 	Displ spiral fx shaft of l femr, 7thN	61	324810	8a230bfe-c6c6
Mycat	Lovastatin	WhiskeyRomeoUniform CharlieYankeeLima	Displ oblique fx shaft of unsp tibia, 7thQ	43	125530	06f80b2c-bda6
Mycat	Lovastatin	 SierraYankeeWhiskeyRomeo CharlieLima	Unsp inj intrns musc/fasc/tend l lit fngr at wrs/hnd lv,subs	100	568534	8a230bfe-c6c6
Mycat	Lovastatin	LimaCharlie HotelRomeoYankeeSierra 	Other superficial bite of right ring finger, init encntr	33	738887	06f80b2c-bda6
Jayo	GOLDENROD	 Romeo UniformLima Hotel	Vertebral artery compression syndromes, site unspecified	76	336909	06f80b2c-bda6
Jayo	GOLDENROD	SierraHotelLima 	Exposure to s	85	259569	2c8cfc88-530f
Jayo	GOLDENROD	 RomeoLimaYankee SierraCharlie	Disp fx of medial phalanx of left middle finger, sequela	53	609306	2c8cfc88-530f
\.


--
-- Data for Name: food_category; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.food_category (id, name) FROM stdin;
70520393-c512	entecavir
06f80b2c-bda6	Standardized Allergenic
69a47987-d54b	Sodium Chloride
8a230bfe-c6c6	Acetaminophen, Diphenhydramine HCl
2c8cfc88-530f	Ropinirole Hydrochloride
\.


--
-- Data for Name: food_ingredients; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.food_ingredients (rname, rbranch, foodname, ingredient) FROM stdin;
Skynoodle	Glyburide	 Form	VkH2TLTgFo
Skynoodle	Glyburide	Uniform Whiskey Lima	IADoEkfNza
Skynoodle	Glyburide	 Hotel	2mXgB4oAbG
Skynoodle	Glyburide	Yankee Romeo Uniform Hotel 	xZ4CC4mwfC
Yacero	THE	 Uniform Hotel Lima 	y3XITLnubD
Yacero	THE	Romeo Hotel Lima	eNnWiKitVF
Yacero	THE	 Hotel Uniform 	fNbEzDh1a1
Trudoo	Lamotrigine	 Lima 	vxyJADR2ED
Trudoo	Lamotrigine	 Uniform Lima Sierra Hotel	cftMswxHBg
Trudoo	Lamotrigine	Yankee Charlie UniformHotel 	8Djf9F6OJQ
Trudoo	Lamotrigine	 Hotel LimaRomeo	c7sfWjq7ir
Yacero	THE	LimaRomeo	OwNigiN0Nj
Mycat	Lovastatin	Uniform 	OijcDHVdit
Mycat	Lovastatin	WhiskeyRomeoUniform CharlieYankeeLima	aEwwVs1XEW
Mycat	Lovastatin	 SierraYankeeWhiskeyRomeo CharlieLima	AfjNw6AuAC
Mycat	Lovastatin	LimaCharlie HotelRomeoYankeeSierra 	FfSt8kCZfp
Tagopia	Headache	 Romeo Hotel Uniform	mjbdngUj3T
Tagopia	Headache	HotelLimaSierraYankee	LSFyef6lzg
Tagopia	Headache	 Hotel RomeoLimaUniformCharlie	vEyr34KYDw
Tagopia	Headache	HotelYankee Uniform	jE2B74zXhM
Meevee	Levaquin	 Charlie YankeeLima Romeo 	VkH2TLTgFo
Meevee	Levaquin	LimaUniform Hotel	IADoEkfNza
Meevee	Levaquin	 UniformRomeoYankee 	2mXgB4oAbG
Meevee	Levaquin	 LimaCharlieYankeeRomeoSierraUniform	xZ4CC4mwfC
Feednation	DEXTROSE	HotelUniform SierraRomeo 	y3XITLnubD
Feednation	DEXTROSE	Uniform Lima HotelRomeo	eNnWiKitVF
Feednation	DEXTROSE	HotelCharlieUniform	fNbEzDh1a1
Feednation	DEXTROSE	 Romeo 	vxyJADR2ED
Jayo	GOLDENROD	SierraHotelLima 	cftMswxHBg
Jayo	GOLDENROD	 Romeo UniformLima Hotel	8Djf9F6OJQ
\.


--
-- Data for Name: ingredient; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.ingredient (id, name) FROM stdin;
VkH2TLTgFo	nectar
IADoEkfNza	coconut oil
2mXgB4oAbG	anise
xZ4CC4mwfC	sweet potato
y3XITLnubD	chip
eNnWiKitVF	salad
fNbEzDh1a1	Goji berry
vxyJADR2ED	coconut oil
cftMswxHBg	rice
8Djf9F6OJQ	citrus
c7sfWjq7ir	potato chip
OwNigiN0Nj	soy milk
OijcDHVdit	coleslaw
aEwwVs1XEW	coriander
AfjNw6AuAC	mascarpone
FfSt8kCZfp	black olive
mjbdngUj3T	oats
LSFyef6lzg	peaches
vEyr34KYDw	baguette
jE2B74zXhM	parsnip
\.


--
-- Data for Name: min_transaction_promo; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.min_transaction_promo (id, minimumtransactionnum) FROM stdin;
P-10	2
P-5	2
P-20	4
P-30	6
P-35	10
RO-3	3
RO-5	5
RO-10	10
RO-15	15
RO-20+	20
\.


--
-- Data for Name: payment_method; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.payment_method (id, name) FROM stdin;
hyeG2VznuH	Cash
B32DHWKN8n	Virtual account
ECE4TdgcHi	Debit cards.
gCr4Exhk1Q	Credit cards.
JPXAR9qkUC	Bank transfers
\.


--
-- Data for Name: payment_status; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.payment_status (id, name) FROM stdin;
vq63gaILPd	Complete
SzKzmHaqm1	Pending
F8LCGrKFTm	Cancelled
JmXjbmrmMB	Refunded
SyR3chyrKs	Failed
\.


--
-- Data for Name: promo; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.promo (id, promoname, discount) FROM stdin;
P-10	HEMAT 10%	10
P-5	HEMAT 5%	5
P-20	HEMAT 20%	20
P-30	HEMAT 30%	30
P-35	HEMAT 35%	35
RO-3	Repeat Order 3x	2
RO-5	Repeat Order 5x	3
RO-10	Repeat Order 10x	7
RO-15	Repeat Order 15x	10
RO-20+	Repeat Order 20x+	15
10-10	10.10 diskon 10%	10
11-11	11.11 diskon 11%	11
12-12	12.12 diskon 12%	12
9-9	09.09 diskon 9%	9
CNY-10	CNY 10%	10
xmas-30	natal ceria	30
new-year-50	tahun baru	50
fitri-30	eid mubarak	30
ramadan-15	ramadan berkah	15
jkt-fair-22	jakarta fair	20
\.


--
-- Data for Name: restaurant; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.restaurant (rname, rbranch, email, rphonenum, street, district, city, province, rating, rcategory) FROM stdin;
Skynoodle	Glyburide	mriccardi5@1688.com	746-903-3167	Oak	Lane	Segbwema	Sierra Leone	8	4f8480b2-235d
Livetube	Good	mriccardi5@1688.com	805-883-9296	Heffernan	Court	Thành Phố Hà Giang	Vietnam	0	4f8480b2-235d
Yacero	THE	mriccardi5@1688.com	826-683-0389	Lake View	Place	Kurikka	Finland	5	4f8480b2-235d
Trudoo	Lamotrigine	mriccardi5@1688.com	404-565-6219	Starling	Road	Dalongzhan	China	8	63dc4e25-725f
Zoonder	Healthy	mriccardi5@1688.com	115-569-2315	Summer Ridge	Road	Biryulëvo Zapadnoye	Russia	0	4f8480b2-235d
Flipstorm	Carisoprodol	mriccardi5@1688.com	590-417-6884	Milwaukee	Terrace	Guaíra	Brazil	7	4f8480b2-235d
Skyndu	Phendimetrazine	fpatient6@engadget.com	554-799-8432	Buhler	Terrace	Zoumaping	China	4	63dc4e25-725f
Vinte	Vamousse	fpatient6@engadget.com	913-180-3367	7th	Parkway	Melati	Indonesia	1	63dc4e25-725f
Bubblebox	Cortisone	fpatient6@engadget.com	962-694-4053	Rockefeller	Parkway	Baocun	China	5	63dc4e25-725f
Browsecat	Drainage	fpatient6@engadget.com	308-275-1567	Sunbrook	Hill	Sihai	China	0	80108a61-c5f0
Izio	Multi	fpatient6@engadget.com	184-844-7741	Lyons	Lane	Kisarawe	Tanzania	10	80108a61-c5f0
Vinte	HYPERPIGMENTATION	fpatient6@engadget.com	501-480-6799	Manufacturers	Place	Florencia	Colombia	1	4f8480b2-235d
Feedspan	ATOMY 	ehordle7@google.co.uk	628-532-2479	Lakeland	Center	Xiema	China	10	80108a61-c5f0
Janyx	dg	ehordle7@google.co.uk	204-744-9583	Kropf	Circle	Lewodoli	Indonesia	5	80108a61-c5f0
Shuffledrive	Chinese	ehordle7@google.co.uk	686-274-0196	Rigney	Street	Petani	Indonesia	9	80108a61-c5f0
Meevee	Levaquin	ehordle7@google.co.uk	554-380-5599	Schlimgen	Terrace	Huangcun	China	6	80108a61-c5f0
Plambee	Icy	ehordle7@google.co.uk	603-876-5738	Starling	Way	Rameshki	Russia	8	80108a61-c5f0
Voomm	Clonidine	ehordle7@google.co.uk	170-496-6145	Nelson	Point	Shujāābād	Pakistan	9	03961711-6e0d
Yoveo	Levofloxacin	rbrehault8@cyberchimps.com	995-724-8612	Sherman	Hill	Bilao	Philippines	1	03961711-6e0d
Eabox	Amlodipine	rbrehault8@cyberchimps.com	449-127-5318	Hovde	Hill	Muriaé	Brazil	3	03961711-6e0d
Gigazoom	Nicotine	rbrehault8@cyberchimps.com	428-283-4292	Butterfield	Avenue	Quanzhou	China	0	80108a61-c5f0
Feednation	DEXTROSE	rbrehault8@cyberchimps.com	881-836-8192	Oakridge	Avenue	Bogorejo	Indonesia	3	03961711-6e0d
Skinder	FUROSEMIDE	rbrehault8@cyberchimps.com	990-282-5288	Quincy	Street	Rosario del Ingre	Bolivia	4	03961711-6e0d
Tagopia	Headache	rbrehault8@cyberchimps.com	856-824-4916	Huxley	Center	Hekou	China	7	03961711-6e0d
Mycat	Lovastatin	tmarkham9@sbwire.com	968-711-5679	Ridge Oak	Place	Maikun	China	0	80108a61-c5f0
Trilith	Alprazolam	tmarkham9@sbwire.com	324-355-7480	Pond	Park	Kundung	Indonesia	1	03961711-6e0d
Edgeblab	SHISEIDO	tmarkham9@sbwire.com	676-487-1758	Lotheville	Lane	Thị Trấn Cao Lộc	Vietnam	8	03961711-6e0d
Jayo	GOLDENROD	tmarkham9@sbwire.com	765-704-1783	Lukken	Way	Alvega	Portugal	3	80108a61-c5f0
Kamba	Lungs	ckieffa@hugedomains.com	149-705-1876	Crest Line	Hill	Waiwukak	Indonesia	2	7fdb70b4-8d0d
Skyndu	Risperidone	ckieffa@hugedomains.com	905-520-4969	Ridgeview	Place	Kurchatov	Russia	1	7fdb70b4-8d0d
Fliptune	Mango	ckieffa@hugedomains.com	144-314-7705	Daystar	Center	Pedro II	Brazil	8	63dc4e25-725f
Yakidoo	Pleo Rub	ckieffa@hugedomains.com	681-915-3090	Dunning	Alley	Tarbes	France	9	4f8480b2-235d
Shufflebeat	Arizona	ckieffa@hugedomains.com	329-898-8787	3rd	Lane	Hagfors	Sweden	3	80108a61-c5f0
Photobug	PRAVASTATIN	ckieffa@hugedomains.com	581-501-0965	Sloan	Avenue	San Francisco	Honduras	7	7fdb70b4-8d0d
Dazzlesphere	Hydroxyzine	ckieffa@hugedomains.com	542-433-9876	Morrow	Court	Bitaogan	Philippines	8	4f8480b2-235d
Yamia	Quercetin	gdulanyb@accuweather.com	593-987-7494	Waywood	Pass	Maiorca	Portugal	3	4f8480b2-235d
Edgeclub	Degree	gdulanyb@accuweather.com	397-143-8880	Erie	Point	Shums’k	Ukraine	7	80108a61-c5f0
Voolia	GENOTROPIN	gdulanyb@accuweather.com	244-848-0012	Graedel	Way	Shanguang	China	10	80108a61-c5f0
Katz	Infants	gdulanyb@accuweather.com	823-931-5373	Oxford	Park	Verkhniy Yasenov	Ukraine	0	03961711-6e0d
Realbuzz	Bupropion	gsawfootc@blogs.com	808-380-8075	Rigney	Way	Hilversum	Netherlands	8	80108a61-c5f0
Edgepulse	FLUDROCORTISONE	gsawfootc@blogs.com	827-213-1372	Montana	Alley	Tunggulsari	Indonesia	6	7fdb70b4-8d0d
Jazzy	Hydrocodone	gsawfootc@blogs.com	604-614-2227	Dawn	Plaza	Zaoshi	China	0	80108a61-c5f0
Mycat	ERYTHROMYCIN	gsawfootc@blogs.com	447-337-4068	Westend	Center	Bieniewice	Poland	2	80108a61-c5f0
Quinu	Lithium	zallamd@deliciousdays.com	667-950-5892	Sullivan	Junction	Karangsari	Indonesia	5	7fdb70b4-8d0d
Dabshots	Anticavity	zallamd@deliciousdays.com	384-826-4307	Scofield	Drive	Burnaby	Canada	6	7fdb70b4-8d0d
Youspan	50 Person	zallamd@deliciousdays.com	641-721-5658	Melby	Alley	Viña del Mar	Chile	8	7fdb70b4-8d0d
Gabvine	Hand	zallamd@deliciousdays.com	993-638-5760	Mallory	Plaza	Borūjen	Iran	7	7fdb70b4-8d0d
Buzzster	Nisoldipine	mcescottie@posterous.com	528-442-3982	Mesta	Court	Lohayong	Indonesia	8	03961711-6e0d
Babbleopia	QUALITY	mcescottie@posterous.com	628-210-5139	Bluestem	Trail	Gayam	Indonesia	9	7fdb70b4-8d0d
Twinder	HYDROCODONE	mcescottie@posterous.com	919-164-6534	Lindbergh	Center	Durham	United States	6	7fdb70b4-8d0d
\.


--
-- Data for Name: restaurant_category; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.restaurant_category (id, name) FROM stdin;
4f8480b2-235d	Stim
63dc4e25-725f	Bitchip
80108a61-c5f0	Duobam
03961711-6e0d	It
7fdb70b4-8d0d	Andalax
\.


--
-- Data for Name: restaurant_operating_hours; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.restaurant_operating_hours (name, branch, day, starthours, endhours) FROM stdin;
Jayo	GOLDENROD	Monday	01:00:00	17:10:00
Jayo	GOLDENROD	Wednesday	01:05:00	14:59:00
Jayo	GOLDENROD	Sunday	10:14:00	14:13:00
Jayo	GOLDENROD	Tuesday	11:05:00	18:35:00
Jayo	GOLDENROD	Saturday	01:54:00	19:12:00
Mycat	Lovastatin	Thursday	04:01:00	19:42:00
Mycat	Lovastatin	Saturday	02:23:00	13:37:00
Mycat	Lovastatin	Sunday	05:56:00	23:07:00
Mycat	Lovastatin	Tuesday	10:58:00	21:28:00
Mycat	Lovastatin	Monday	10:51:00	21:56:00
Feednation	DEXTROSE	Sunday	06:02:00	15:51:00
Feednation	DEXTROSE	Monday	02:44:00	20:38:00
Feednation	DEXTROSE	Thursday	10:43:00	23:29:00
Feednation	DEXTROSE	Wednesday	10:23:00	14:56:00
Yoveo	Levofloxacin	Wednesday	05:49:00	15:26:00
Yoveo	Levofloxacin	Sunday	09:37:00	12:34:00
Yoveo	Levofloxacin	Saturday	06:32:00	16:08:00
Yoveo	Levofloxacin	Tuesday	06:44:00	12:58:00
Tagopia	Headache	Saturday	03:03:00	14:49:00
Tagopia	Headache	Monday	06:55:00	19:31:00
Tagopia	Headache	Friday	11:45:00	12:36:00
Tagopia	Headache	Tuesday	01:33:00	12:17:00
Meevee	Levaquin	Friday	04:08:00	13:34:00
Meevee	Levaquin	Wednesday	00:46:00	16:00:00
Meevee	Levaquin	Thursday	10:30:00	12:15:00
Meevee	Levaquin	Sunday	00:48:00	18:06:00
Trudoo	Lamotrigine	Wednesday	03:54:00	14:26:00
Trudoo	Lamotrigine	Thursday	10:39:00	17:26:00
Trudoo	Lamotrigine	Tuesday	07:47:00	18:44:00
Trudoo	Lamotrigine	Monday	08:33:00	12:08:00
Yacero	THE	Monday	04:39:00	23:56:00
Yacero	THE	Friday	07:04:00	14:12:00
Yacero	THE	Thursday	09:30:00	23:05:00
Yacero	THE	Sunday	03:47:00	13:39:00
Yacero	THE	Wednesday	08:38:00	14:02:00
\.


--
-- Data for Name: restaurant_promo; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.restaurant_promo (rname, rbranch, pid, start, "end") FROM stdin;
Skynoodle	Glyburide	P-10	2022-08-02 00:00:00	2022-01-18 00:00:00
Skynoodle	Glyburide	P-5	2021-11-07 00:00:00	2022-04-12 00:00:00
Skynoodle	Glyburide	P-20	2022-01-01 00:00:00	2021-12-21 00:00:00
Skynoodle	Glyburide	P-30	2021-11-26 00:00:00	2022-07-06 00:00:00
Yacero	THE	P-35	2022-10-06 00:00:00	2022-03-10 00:00:00
Yacero	THE	RO-3	2022-02-03 00:00:00	2022-07-08 00:00:00
Yacero	THE	RO-5	2021-11-11 00:00:00	2022-06-04 00:00:00
Yacero	THE	RO-10	2022-01-19 00:00:00	2022-05-16 00:00:00
Trudoo	Lamotrigine	RO-15	2022-05-11 00:00:00	2022-02-21 00:00:00
Trudoo	Lamotrigine	RO-20+	2022-01-09 00:00:00	2022-08-17 00:00:00
\.


--
-- Data for Name: special_day_promo; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.special_day_promo (id, datetime) FROM stdin;
10-10	2022-10-10
11-11	2022-11-11
12-12	2022-12-12
9-9	2022-09-09
CNY-10	2022-02-05
xmas-30	2022-12-25
new-year-50	2022-01-01
fitri-30	2022-05-12
ramadan-15	2022-04-17
jkt-fair-22	2022-06-26
\.


--
-- Data for Name: temp; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.temp (rname, rbranch, foodname, pid, start, "end") FROM stdin;
Skynoodle	Glyburide	 Form	P-10	2022-08-02 00:00:00	2022-01-18 00:00:00
Skynoodle	Glyburide	Uniform Whiskey Lima	P-5	2021-11-07 00:00:00	2022-04-12 00:00:00
Skynoodle	Glyburide	 Hotel	P-20	2022-01-01 00:00:00	2021-12-21 00:00:00
Skynoodle	Glyburide	Yankee Romeo Uniform Hotel 	P-30	2021-11-26 00:00:00	2022-07-06 00:00:00
Yacero	THE	 Uniform Hotel Lima 	P-35	2022-10-06 00:00:00	2022-03-10 00:00:00
Yacero	THE	LimaRomeo	RO-3	2022-02-03 00:00:00	2022-07-08 00:00:00
Yacero	THE	Romeo Hotel Lima	RO-5	2021-11-11 00:00:00	2022-06-04 00:00:00
Yacero	THE	 Hotel Uniform 	RO-10	2022-01-19 00:00:00	2022-05-16 00:00:00
Trudoo	Lamotrigine	 Lima 	RO-15	2022-05-11 00:00:00	2022-02-21 00:00:00
Trudoo	Lamotrigine	 Uniform Lima Sierra Hotel	RO-20+	2022-01-09 00:00:00	2022-08-17 00:00:00
\.


--
-- Data for Name: transaction; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.transaction (email, datetime, street, district, city, province, totalfood, totaldiscount, deliveryfee, totalprice, rating, pmid, psid, dfid, courierid, vehicletype) FROM stdin;
pcumeskya@columbia.edu	2022-01-06 21:42:38	3419 Woodland Terrace	Alabama	Monsey	Virginia	10	10	15	15.5729166666666003	5	hyeG2VznuH	vq63gaILPd	x9LN21jUNb	mboyatm@feedburner.com	Mobil
rhyndn@posterous.com	2022-04-30 08:09:42	4147 Radford Street	Alaska	New York	New York	6	11	15	15.5729166666666003	5	B32DHWKN8n	SzKzmHaqm1	MrNHF5fUhz	sbraunfeldi@weebly.com	Mobil
lgeekinp@bandcamp.com	2022-10-16 06:46:12	820 Rubaiyat Road	American Samoa	Gladys	California	2	12	15	15.5729166666666003	5	ECE4TdgcHi	F8LCGrKFTm	rbIbekPXfq	gstaddartr@reference.com	Mobil
sfritchlyl@dailymail.co.uk	2022-02-14 03:38:05	2579 Blue Spruce Lane	Arizona	Escalon	Texas	7	12	15	19.7138888888887998	5	gCr4Exhk1Q	JmXjbmrmMB	VAxb5ptyYr	nwinckwortho@imageshack.us	Mobil
bpimbleyq@hhs.gov	2022-07-20 17:27:20	4115 Penn Street	Arkansas	Mcallen	Michigan	7	12	17	18.7555555555554996	5	JPXAR9qkUC	SyR3chyrKs	57L0H5CX68	cglasbeyk@foxnews.com	Mobil
baitchisonj@newyorker.com	2022-05-26 12:56:10	4408 Davis Street	California	Marquette	Utah	10	15	18	27.7972222222221994	4	hyeG2VznuH	vq63gaILPd	L4Jj5kHCW4	mboyatm@feedburner.com	Mobil
htufts@hubpages.com	2022-05-07 04:56:21	432 Black Oak Hollow Road	Colorado	Salinas	Maryland	8	15	18	24.8388888888887998	4	B32DHWKN8n	SzKzmHaqm1	JoHV435OwO	sbraunfeldi@weebly.com	Mobil
bmacalpyneh@mac.com	2022-01-18 07:22:57	4305 Tori Lane	Connecticut	Allenton	Mississippi	2	15	18	16.8805555555554996	4	ECE4TdgcHi	F8LCGrKFTm	FMXOzFTJC2	gstaddartr@reference.com	Mobil
akobierag@cmu.edu	2022-06-29 15:22:00	1823 Adamsville Road	Delaware	Escalon	Pennsylvania	9	10	19	20.9222222222221994	4	gCr4Exhk1Q	JmXjbmrmMB	HVsrVpnAMC	nwinckwortho@imageshack.us	Mobil
bsturgeonf@tuttocitta.it	2022-07-15 20:19:45	1344 Richards Avenue	District of Columbia	Mcallen	Arkansas	5	10	19	16.9638888888887998	4	JPXAR9qkUC	SyR3chyrKs	EimwxrdNbn	cglasbeyk@foxnews.com	Mobil
\.


--
-- Data for Name: transaction_actor; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.transaction_actor (email, nik, bankname, accountno, restopay, adminid) FROM stdin;
spritchett5@earthlink.net	6863312196527351	Meevee	8379607491012530	3414659	rhuskinson0@opensource.org
tbranchet6@google.co.jp	3329679108170664	Wikizz	8474698833440280	8610786	cmcileen1@usda.gov
rheinreich7@liveinternet.ru	1927975622584729	Zoovu	6825825169165363	5013379	rhuskinson0@opensource.org
kgosdin9@aboutads.info	5318941495372182	Jabberbean	2959746124161583	4566632	cmcileen1@usda.gov
lhandrekt@google.co.jp	4778105792656044	Eire	294741496227424	4764389	rhuskinson0@opensource.org
dkroonc@google.com.au	1246023607076900	Camido	5021938981147978	8453864	cmcileen1@usda.gov
rmoncrefeb@businesswire.com	6749770891168319	InnoZ	3408283798224251	3276547	rhuskinson0@opensource.org
mgallgherd@unblog.fr	1532105274156288	Twitterwire	7456004206531102	7005148	cmcileen1@usda.gov
hsimcoe@vimeo.com	4408362206697196	Edgepulse	8064464004558044	7756297	rhuskinson0@opensource.org
bsturgeonf@tuttocitta.it	4406330652681355	Oyonder	791313330043701	3508984	cmcileen1@usda.gov
akobierag@cmu.edu	8821528206217872	Divape	7781224752304236	6627289	rhuskinson0@opensource.org
bmacalpyneh@mac.com	2237510666204888	Skajo	5416167418457610	5140844	cmcileen1@usda.gov
sbraunfeldi@weebly.com	1804771375007560	Skalith	7858883346978014	2694742	rhuskinson0@opensource.org
baitchisonj@newyorker.com	6952237302528556	Realbridge	8848062752083002	1267001	abachman2@yahoo.co.jp
cglasbeyk@foxnews.com	6233040412247031	Buzzdog	7606830419789530	7280670	cmcileen1@usda.gov
sfritchlyl@dailymail.co.uk	6385803013850295	Tagopia	2389134357547422	3070397	lashbolt3@tamu.edu
mboyatm@feedburner.com	6484534341179314	Twimm	7357982088936828	2758881	lashbolt3@tamu.edu
rhyndn@posterous.com	3844343052370986	Ooba	3211373384698571	8502434	psiegertsz4@zdnet.com
nwinckwortho@imageshack.us	3018407389469023	Divanoodle	3780452881097936	9951581	psiegertsz4@zdnet.com
gstaddartr@reference.com	6351412576172144	JumpXS	8986083550287412	5789939	psiegertsz4@zdnet.com
arapkins8@reddit.com	1370636350672841	Innojam	1729570117443661	4724902	lashbolt3@tamu.edu
pcumeskya@columbia.edu	3092799385699701	Twitterbridge	3776577673536866	2002450	cmcileen1@usda.gov
lgeekinp@bandcamp.com	4400723799580085	Nlounge	6219333588802570	2855236	rhuskinson0@opensource.org
bpimbleyq@hhs.gov	6732500294044204	Buzzbean	2351953443148719	8879570	rhuskinson0@opensource.org
htufts@hubpages.com	5315757064426577	Edgepulse	2135323649372526	7696009	lashbolt3@tamu.edu
ewycliffe1@dropbox.com	2379637002931902	Teklist	8320781043278136	8549711	psiegertsz4@zdnet.com
dmasurel0@etsy.com	3133137368209055	Dabjam	4634276736269710	2610569	abachman2@yahoo.co.jp
bbarkly2@si.edu	2100616376287052	Tagchat	9740938378399559	6181019	abachman2@yahoo.co.jp
nbreward3@walmart.com	5229186803771554	Meejo	7451706108510471	3409519	cmcileen1@usda.gov
dpetrie4@twitpic.com	4571988543037884	Aivee	5238214568529733	9998391	lashbolt3@tamu.edu
mriccardi5@1688.com	7539088515252393	Leexo	6385442838704489	6528148	abachman2@yahoo.co.jp
fpatient6@engadget.com	2041892259458495	Meevee	4943809839360049	8792756	psiegertsz4@zdnet.com
ehordle7@google.co.uk	2853284611327222	Realblab	4661859393779571	7415880	cmcileen1@usda.gov
rbrehault8@cyberchimps.com	7591834412304767	Shufflebeat	9570903453615653	9580284	abachman2@yahoo.co.jp
tmarkham9@sbwire.com	9163364199146094	Quamba	1781502783775553	5387632	cmcileen1@usda.gov
ckieffa@hugedomains.com	9740786023824560	Kimia	5742297785698680	8163700	psiegertsz4@zdnet.com
gdulanyb@accuweather.com	5906187487380606	Realbridge	6993746553567207	1781156	psiegertsz4@zdnet.com
gsawfootc@blogs.com	8384830276813291	Topicblab	5943708274578203	6368484	cmcileen1@usda.gov
zallamd@deliciousdays.com	6732616596485461	Fadeo	2298245954562464	3663373	rhuskinson0@opensource.org
mcescottie@posterous.com	4225259107646049	Edgeblab	6725924365368666	6726501	abachman2@yahoo.co.jp
\.


--
-- Data for Name: transaction_food; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.transaction_food (email, datetime, rname, rbranch, foodname, amount, note) FROM stdin;
pcumeskya@columbia.edu	2022-01-06 21:42:38	Skynoodle	Glyburide	 Form	85	Vivamus vel nulla eget eros elementum pellentesque.
rhyndn@posterous.com	2022-04-30 08:09:42	Skynoodle	Glyburide	Uniform Whiskey Lima	46	Duis ac nibh. Fusce lacus purus.
lgeekinp@bandcamp.com	2022-10-16 06:46:12	Skynoodle	Glyburide	 Hotel	64	Nullam sit amet turpis elementum ligula vehicula consequat.
sfritchlyl@dailymail.co.uk	2022-02-14 03:38:05	Skynoodle	Glyburide	Yankee Romeo Uniform Hotel 	18	Nunc rhoncus dui vel sem. 
bpimbleyq@hhs.gov	2022-07-20 17:27:20	Yacero	THE	 Uniform Hotel Lima 	55	Aenean sit amet justo. Morbi ut odio. Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo.
baitchisonj@newyorker.com	2022-05-26 12:56:10	Yacero	THE	LimaRomeo	55	Nullam sit amet turpis elementum ligula vehicula consequat.
htufts@hubpages.com	2022-05-07 04:56:21	Yacero	THE	Romeo Hotel Lima	76	Quisque ut erat. Curabitur gravida nisi at nibh. 
bmacalpyneh@mac.com	2022-01-18 07:22:57	Yacero	THE	 Hotel Uniform 	29	Suspendisse potenti. Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum. Aliquam non mauris.
akobierag@cmu.edu	2022-06-29 15:22:00	Trudoo	Lamotrigine	 Lima 	21	Nulla ut erat id mauris vulputate elementum.
bsturgeonf@tuttocitta.it	2022-07-15 20:19:45	Trudoo	Lamotrigine	Yankee Charlie UniformHotel 	23	Lorem ipsum dolor sit amet
\.


--
-- Data for Name: transaction_history; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.transaction_history (email, datetime, tsid, datetimestatus) FROM stdin;
pcumeskya@columbia.edu	2022-01-06 21:42:38	B19AKOKWW	2022-02-17 00:00:00
rhyndn@posterous.com	2022-04-30 08:09:42	X19DBUSBDU	2022-06-08 00:00:00
lgeekinp@bandcamp.com	2022-10-16 06:46:12	Z11SNJSHDG	2022-10-22 00:00:00
sfritchlyl@dailymail.co.uk	2022-02-14 03:38:05	C23AOKKWO	2022-06-28 00:00:00
bpimbleyq@hhs.gov	2022-07-20 17:27:20	X32SSSUUBB	2022-08-16 00:00:00
baitchisonj@newyorker.com	2022-05-26 12:56:10	B19DWDEFDS	2022-01-27 00:00:00
htufts@hubpages.com	2022-05-07 04:56:21	X14DCCESEW	2021-12-01 00:00:00
bmacalpyneh@mac.com	2022-01-18 07:22:57	Z11DDFEWGF	2022-05-01 00:00:00
akobierag@cmu.edu	2022-06-29 15:22:00	C24KOSOWKO	2021-10-31 00:00:00
bsturgeonf@tuttocitta.it	2022-07-15 20:19:45	C13DQIHDWDF	2022-06-06 00:00:00
\.


--
-- Data for Name: transaction_status; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.transaction_status (id, name) FROM stdin;
B19AKOKWW	Complete
X19DBUSBDU	Pending
Z11SNJSHDG	Cancelled
C23AOKKWO	Failed
X32SSSUUBB	Refunded
B19DWDEFDS	Complete
X14DCCESEW	Pending
Z11DDFEWGF	Cancelled
C24KOSOWKO	Failed
C13DQIHDWDF	Refunded
\.


--
-- Data for Name: user_acc; Type: TABLE DATA; Schema: sirest; Owner: db22b006
--

COPY sirest.user_acc (email, password, phonenum, fname, lname) FROM stdin;
rhuskinson0@opensource.org	rgaiKW6pi	3553514140	Rakel	Huskinson
cmcileen1@usda.gov	Y0AYWBUde	7917462874	Cristen	McIleen
abachman2@yahoo.co.jp	zIQRL06	9325858810	Amie	Bachman
lashbolt3@tamu.edu	DtxiHx8	3028997236	Lon	Ashbolt
psiegertsz4@zdnet.com	GSkPqI	9585182044	Phebe	Siegertsz
spritchett5@earthlink.net	9lWso0tzM	5176454873	Salomo	Pritchett
tbranchet6@google.co.jp	BmX1L85Xs	1768249239	Tory	Branchet
rheinreich7@liveinternet.ru	SVkOWwDJCoxf	1682149067	Roth	Heinreich
arapkins8@reddit.com	V7lXENqjb	6693362224	Ara	Rapkins
kgosdin9@aboutads.info	26dbwZ	7957679748	Kerry	Gosdin
pcumeskya@columbia.edu	cMpsPFB22	5787367648	Preston	Cumesky
rmoncrefeb@businesswire.com	jWQnRSPvK	8483110885	Raphael	Moncrefe
dkroonc@google.com.au	0Ebtn7B	1742728230	Dennet	Kroon
mgallgherd@unblog.fr	SCICuc	8365774868	Marti	Gallgher
hsimcoe@vimeo.com	BAi1WNMKiCI	4664618294	Hans	Simco
bsturgeonf@tuttocitta.it	2r7GJFuy	9648705676	Bennie	Sturgeon
akobierag@cmu.edu	GsLpoTO	1541387369	Andres	Kobiera
bmacalpyneh@mac.com	DF2uhMd	6078425750	Brear	MacAlpyne
sbraunfeldi@weebly.com	u3LoYNFx	5897452415	Shaylyn	Braunfeld
baitchisonj@newyorker.com	lMSAmBsIbG	8483142515	Bianka	Aitchison
cglasbeyk@foxnews.com	Wg6Z9Da	6521133607	Clerkclaude	Glasbey
sfritchlyl@dailymail.co.uk	x4F6aH	1526743811	Sara-ann	Fritchly
mboyatm@feedburner.com	0odznz4DA9b	4847939365	Martelle	Boyat
rhyndn@posterous.com	92Ug9z13	9243474780	Roxi	Hynd
nwinckwortho@imageshack.us	GXOjIsNw	2241566291	Nicoline	Winckworth
lgeekinp@bandcamp.com	OXzi0YCR61i	4182937600	Lay	Geekin
bpimbleyq@hhs.gov	uWpXZf8c	6501147326	Berny	Pimbley
gstaddartr@reference.com	ltcdcF	8047448755	Gilbertine	Staddart
htufts@hubpages.com	uzbsKeB36M8	6462042871	Herschel	Tuft
lhandrekt@google.co.jp	zDsHSvuL	9816193504	Lin	Handrek
dmasurel0@etsy.com	yQ6oOZ	1671999474	Delcine	Masurel
ewycliffe1@dropbox.com	jwNyBRXJE3Pz	4284447507	Evangelin	Wycliffe
bbarkly2@si.edu	qdOFqkBhuz1Z	6661303147	Bonnie	Barkly
nbreward3@walmart.com	6nn0ytQxv0V	7308838402	Neal	Breward
dpetrie4@twitpic.com	lXpbHou	7938875291	Dante	Petrie
mriccardi5@1688.com	3ELli8gY0p4	5409076020	Merci	Riccardi
fpatient6@engadget.com	nEV9BbB	7632445322	Fernanda	Patient
ehordle7@google.co.uk	Ey36c4JIRqk5	2904051736	Etti	Hordle
rbrehault8@cyberchimps.com	yJLBnlOfNI	1957655440	Rog	Brehault
tmarkham9@sbwire.com	J6xJrWTdtw	6127420090	Terrel	Markham
ckieffa@hugedomains.com	nnuX0ZlT7	5783512983	Christin	Kieff
gdulanyb@accuweather.com	hIUdwmCTqZ0	8961706314	Glenden	Dulany
gsawfootc@blogs.com	3TMZA4NB6	5363963487	Garrett	Sawfoot
zallamd@deliciousdays.com	oTodYtt	3916622642	Zilvia	Allam
mcescottie@posterous.com	X1eLtPmPM	2346893743	Marion	Cescotti
\.


--
-- Name: admin admin_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (email);


--
-- Name: courier courier_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.courier
    ADD CONSTRAINT courier_pkey PRIMARY KEY (email);


--
-- Name: customer customer_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (email);


--
-- Name: delivery_fee_per_km delivery_fee_per_km_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.delivery_fee_per_km
    ADD CONSTRAINT delivery_fee_per_km_pkey PRIMARY KEY (id);


--
-- Name: food_category food_category_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.food_category
    ADD CONSTRAINT food_category_pkey PRIMARY KEY (id);


--
-- Name: food_ingredients food_ingredients_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.food_ingredients
    ADD CONSTRAINT food_ingredients_pkey PRIMARY KEY (rname, rbranch, foodname);


--
-- Name: food food_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.food
    ADD CONSTRAINT food_pkey PRIMARY KEY (rname, rbranch, foodname);


--
-- Name: ingredient ingredient_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.ingredient
    ADD CONSTRAINT ingredient_pkey PRIMARY KEY (id);


--
-- Name: min_transaction_promo min_transaction_promo_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.min_transaction_promo
    ADD CONSTRAINT min_transaction_promo_pkey PRIMARY KEY (id);


--
-- Name: payment_method payment_method_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.payment_method
    ADD CONSTRAINT payment_method_pkey PRIMARY KEY (id);


--
-- Name: payment_status payment_status_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.payment_status
    ADD CONSTRAINT payment_status_pkey PRIMARY KEY (id);


--
-- Name: promo promo_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.promo
    ADD CONSTRAINT promo_pkey PRIMARY KEY (id);


--
-- Name: restaurant_category restaurant_category_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.restaurant_category
    ADD CONSTRAINT restaurant_category_pkey PRIMARY KEY (id);


--
-- Name: restaurant_operating_hours restaurant_operating_hours_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.restaurant_operating_hours
    ADD CONSTRAINT restaurant_operating_hours_pkey PRIMARY KEY (name, branch, day);


--
-- Name: restaurant restaurant_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.restaurant
    ADD CONSTRAINT restaurant_pkey PRIMARY KEY (rname, rbranch);


--
-- Name: restaurant_promo restaurant_promo_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.restaurant_promo
    ADD CONSTRAINT restaurant_promo_pkey PRIMARY KEY (rname, rbranch, pid);


--
-- Name: special_day_promo special_day_promo_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.special_day_promo
    ADD CONSTRAINT special_day_promo_pkey PRIMARY KEY (id);


--
-- Name: temp temp_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.temp
    ADD CONSTRAINT temp_pkey PRIMARY KEY (rname, rbranch, foodname, pid);


--
-- Name: transaction_actor transaction_actor_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.transaction_actor
    ADD CONSTRAINT transaction_actor_pkey PRIMARY KEY (email);


--
-- Name: transaction_food transaction_food_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.transaction_food
    ADD CONSTRAINT transaction_food_pkey PRIMARY KEY (email, datetime, rname, rbranch, foodname);


--
-- Name: transaction_history transaction_history_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.transaction_history
    ADD CONSTRAINT transaction_history_pkey PRIMARY KEY (email, datetime, tsid);


--
-- Name: transaction transaction_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.transaction
    ADD CONSTRAINT transaction_pkey PRIMARY KEY (email, datetime);


--
-- Name: transaction_status transaction_status_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.transaction_status
    ADD CONSTRAINT transaction_status_pkey PRIMARY KEY (id);


--
-- Name: user_acc user_acc_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.user_acc
    ADD CONSTRAINT user_acc_pkey PRIMARY KEY (email);


--
-- Name: user_acc security_pass; Type: TRIGGER; Schema: sirest; Owner: db22b006
--

CREATE TRIGGER security_pass BEFORE INSERT ON sirest.user_acc FOR EACH ROW EXECUTE PROCEDURE sirest.check_password();


--
-- Name: special_day_promo tg_cek_tgl_promo_valid; Type: TRIGGER; Schema: sirest; Owner: db22b006
--

CREATE TRIGGER tg_cek_tgl_promo_valid BEFORE INSERT OR UPDATE ON sirest.special_day_promo FOR EACH ROW EXECUTE PROCEDURE sirest.cek_tgl_promo_valid();


--
-- Name: transaction trigger_cekbiayapengantaran; Type: TRIGGER; Schema: sirest; Owner: db22b006
--

CREATE TRIGGER trigger_cekbiayapengantaran BEFORE INSERT OR UPDATE ON sirest.transaction FOR EACH ROW EXECUTE PROCEDURE sirest.cekbiayapengantaran();


--
-- Name: delivery_fee_per_km trigger_checktarif; Type: TRIGGER; Schema: sirest; Owner: db22b006
--

CREATE TRIGGER trigger_checktarif BEFORE INSERT OR UPDATE ON sirest.delivery_fee_per_km FOR EACH ROW EXECUTE PROCEDURE sirest.checktarif();


--
-- Name: transaction_actor triggercheckbalance; Type: TRIGGER; Schema: sirest; Owner: db22b006
--

CREATE TRIGGER triggercheckbalance BEFORE INSERT OR UPDATE ON sirest.transaction_actor FOR EACH ROW EXECUTE PROCEDURE sirest.checkbalance();


--
-- Name: transaction_status update_restopay; Type: TRIGGER; Schema: sirest; Owner: db22b006
--

CREATE TRIGGER update_restopay AFTER UPDATE ON sirest.transaction_status FOR EACH ROW EXECUTE PROCEDURE sirest.update_restopay();


--
-- Name: admin admin_email_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.admin
    ADD CONSTRAINT admin_email_fkey FOREIGN KEY (email) REFERENCES sirest.user_acc(email);


--
-- Name: courier courier_email_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.courier
    ADD CONSTRAINT courier_email_fkey FOREIGN KEY (email) REFERENCES sirest.transaction_actor(email);


--
-- Name: customer customer_email_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.customer
    ADD CONSTRAINT customer_email_fkey FOREIGN KEY (email) REFERENCES sirest.transaction_actor(email);


--
-- Name: food food_fcategory_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.food
    ADD CONSTRAINT food_fcategory_fkey FOREIGN KEY (fcategory) REFERENCES sirest.food_category(id);


--
-- Name: food_ingredients food_ingredients_ingredient_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.food_ingredients
    ADD CONSTRAINT food_ingredients_ingredient_fkey FOREIGN KEY (ingredient) REFERENCES sirest.ingredient(id);


--
-- Name: food_ingredients food_ingredients_rname_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.food_ingredients
    ADD CONSTRAINT food_ingredients_rname_fkey FOREIGN KEY (rname, rbranch, foodname) REFERENCES sirest.food(rname, rbranch, foodname);


--
-- Name: food food_rname_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.food
    ADD CONSTRAINT food_rname_fkey FOREIGN KEY (rname, rbranch) REFERENCES sirest.restaurant(rname, rbranch);


--
-- Name: min_transaction_promo min_transaction_promo_id_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.min_transaction_promo
    ADD CONSTRAINT min_transaction_promo_id_fkey FOREIGN KEY (id) REFERENCES sirest.promo(id);


--
-- Name: restaurant restaurant_email_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.restaurant
    ADD CONSTRAINT restaurant_email_fkey FOREIGN KEY (email) REFERENCES sirest.transaction_actor(email);


--
-- Name: restaurant_operating_hours restaurant_operating_hours_name_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.restaurant_operating_hours
    ADD CONSTRAINT restaurant_operating_hours_name_fkey FOREIGN KEY (name, branch) REFERENCES sirest.restaurant(rname, rbranch);


--
-- Name: restaurant_promo restaurant_promo_pid_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.restaurant_promo
    ADD CONSTRAINT restaurant_promo_pid_fkey FOREIGN KEY (pid) REFERENCES sirest.promo(id);


--
-- Name: restaurant_promo restaurant_promo_rname_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.restaurant_promo
    ADD CONSTRAINT restaurant_promo_rname_fkey FOREIGN KEY (rname, rbranch) REFERENCES sirest.restaurant(rname, rbranch);


--
-- Name: restaurant restaurant_rcategory_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.restaurant
    ADD CONSTRAINT restaurant_rcategory_fkey FOREIGN KEY (rcategory) REFERENCES sirest.restaurant_category(id);


--
-- Name: special_day_promo special_day_promo_id_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.special_day_promo
    ADD CONSTRAINT special_day_promo_id_fkey FOREIGN KEY (id) REFERENCES sirest.promo(id);


--
-- Name: temp temp_pid_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.temp
    ADD CONSTRAINT temp_pid_fkey FOREIGN KEY (pid) REFERENCES sirest.promo(id);


--
-- Name: temp temp_rname_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.temp
    ADD CONSTRAINT temp_rname_fkey FOREIGN KEY (rname, rbranch, foodname) REFERENCES sirest.food(rname, rbranch, foodname);


--
-- Name: transaction_actor transaction_actor_adminid_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.transaction_actor
    ADD CONSTRAINT transaction_actor_adminid_fkey FOREIGN KEY (adminid) REFERENCES sirest.admin(email);


--
-- Name: transaction_actor transaction_actor_email_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.transaction_actor
    ADD CONSTRAINT transaction_actor_email_fkey FOREIGN KEY (email) REFERENCES sirest.user_acc(email);


--
-- Name: transaction transaction_courierid_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.transaction
    ADD CONSTRAINT transaction_courierid_fkey FOREIGN KEY (courierid) REFERENCES sirest.courier(email);


--
-- Name: transaction transaction_dfid_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.transaction
    ADD CONSTRAINT transaction_dfid_fkey FOREIGN KEY (dfid) REFERENCES sirest.delivery_fee_per_km(id);


--
-- Name: transaction_food transaction_food_email_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.transaction_food
    ADD CONSTRAINT transaction_food_email_fkey FOREIGN KEY (email, datetime) REFERENCES sirest.transaction(email, datetime) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: transaction_food transaction_food_rname_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.transaction_food
    ADD CONSTRAINT transaction_food_rname_fkey FOREIGN KEY (rname, rbranch, foodname) REFERENCES sirest.food(rname, rbranch, foodname) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: transaction_history transaction_history_email_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.transaction_history
    ADD CONSTRAINT transaction_history_email_fkey FOREIGN KEY (email, datetime) REFERENCES sirest.transaction(email, datetime);


--
-- Name: transaction_history transaction_history_tsid_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.transaction_history
    ADD CONSTRAINT transaction_history_tsid_fkey FOREIGN KEY (tsid) REFERENCES sirest.transaction_status(id);


--
-- Name: transaction transaction_pmid_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.transaction
    ADD CONSTRAINT transaction_pmid_fkey FOREIGN KEY (pmid) REFERENCES sirest.payment_method(id);


--
-- Name: transaction transaction_psid_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22b006
--

ALTER TABLE ONLY sirest.transaction
    ADD CONSTRAINT transaction_psid_fkey FOREIGN KEY (psid) REFERENCES sirest.payment_status(id);


--
-- PostgreSQL database dump complete
--


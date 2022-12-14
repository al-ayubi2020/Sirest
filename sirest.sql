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
-- Name: sirest; Type: SCHEMA; Schema: -; Owner: db22a008
--

CREATE SCHEMA sirest;


ALTER SCHEMA sirest OWNER TO db22a008;

--
-- Name: batasperkm(); Type: FUNCTION; Schema: sirest; Owner: db22a008
--

CREATE FUNCTION sirest.batasperkm() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
 BEGIN

  IF (NEW. motorfee < 2000 OR NEW. motorfee > 7000 OR NEW. carfee < 2000 OR NEW. carfee > 7000) THEN
   RAISE EXCEPTION 'Biaya pengiriman harus lebih besar sam dengan 2000 dan lebih kecil sama dengan 7000';
  END IF;
IF (NEW.motorfee >= NEW.carfee) THEN
   RAISE EXCEPTION 'Biaya pengiriman motor harus lebih murah dari pengiriman mobil';
  END IF;
  RETURN NEW;
 END;
$$;


ALTER FUNCTION sirest.batasperkm() OWNER TO db22a008;

--
-- Name: check_date_promo_violation(); Type: FUNCTION; Schema: sirest; Owner: db22a008
--

CREATE OR REPLACE FUNCTION sirest.check_date_promo_violation() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
SELECT RP.Starttime, RP.Endtime
FROM sirest.RESTAURANT_PROMO RP
WHERE RP.PId = NEW.Id;
IF (NEW.Date < RP.Starttime OR NEW.Date > RP.Endtime) THEN
RAISE EXCEPTION 'Maaf, promo tidak dapat diterapkan. Silakan masukkan tanggal yang valid!';
END IF;
RETURN NEW;
END IF;
END;
$$;


ALTER FUNCTION sirest.check_date_promo_violation() OWNER TO db22a008;

--
-- Name: check_password(); Type: FUNCTION; Schema: sirest; Owner: db22a008
--

CREATE FUNCTION sirest.check_password() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF(TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
  IF(NEW.password <> LOWER(NEW.password) AND NEW.password ~ '[0-9]') THEN
   RETURN NEW;
  END IF;
  RAISE EXCEPTION 'Password harus mengandung huruf kapital dan angka';
  RETURN NEW;
        END IF;
 END;
$$;


ALTER FUNCTION sirest.check_password() OWNER TO db22a008;

--
-- Name: check_saldo(); Type: FUNCTION; Schema: sirest; Owner: db22a008
--

CREATE FUNCTION sirest.check_saldo() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF(TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
      IF(NEW.restopay < 0) THEN
       RAISE EXCEPTION 'Saldo kurang';
      END IF;
  RETURN NEW;
        END IF;
 END;
$$;


ALTER FUNCTION sirest.check_saldo() OWNER TO db22a008;

--
-- Name: menambah_restopay(); Type: FUNCTION; Schema: sirest; Owner: db22a008
--

CREATE FUNCTION sirest.menambah_restopay() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    biaya_pengantaran integer;
    total_harga_makanan integer;
    id_kurir text;
    email_restoran text;
BEGIN
    if(NEW.name = 'Pesanan Selesai') then
        select tr.deliveryFee, (tr.totalprice - tr.deliveryFee), tr.courierid, res.email
        into biaya_pengantaran, total_harga_makanan, id_kurir, email_restoran
        from transaction tr
        join transaction_history th on tr.email = th.email
        join transaction_status ts on ts.id = th.tsid
        join transaction_food tf on tf.email = tr.email and tf.datetime = tr.datetime
        join food f on f.rname = tf.rname and f.rbranch = tf.rbranch and f.foodname = tf.foodname
        join restaurant res on res.rname = f.rname and res.rbranch = f.rbranch;

        update transaction_actor set restopay = restopay + biaya_pengantaran
        where email = id_kurir;

        update transaction_actor set restopay = restopay + total_harga_makanan
        where email = email_restoran;
    end if;
    return new;
END;
$$;


ALTER FUNCTION sirest.menambah_restopay() OWNER TO db22a008;

--
-- Name: total(); Type: FUNCTION; Schema: sirest; Owner: db22a008
--

CREATE FUNCTION sirest.total() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
 DECLARE
        TOTAL_BIAYA INT;
 BEGIN

  TOTAL_BIAYA = (total_makanan_harga-total_diskon) +biaya_pengantaran;
  RETURN NEW;
 END;
$$;


ALTER FUNCTION sirest.total() OWNER TO db22a008;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: admin; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.admin (
    email character varying(50) NOT NULL
);


ALTER TABLE sirest.admin OWNER TO db22a008;

--
-- Name: courier; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.courier (
    email character varying(50) NOT NULL,
    platenum character varying(10) NOT NULL,
    drivinglicensenum character varying(20) NOT NULL,
    vehicletype character varying(15) NOT NULL,
    vehiclebrand character varying(15) NOT NULL
);


ALTER TABLE sirest.courier OWNER TO db22a008;

--
-- Name: customer; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.customer (
    email character varying(50) NOT NULL,
    birthdate date NOT NULL,
    sex character(1) NOT NULL
);


ALTER TABLE sirest.customer OWNER TO db22a008;

--
-- Name: delivery_fee_per_km; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.delivery_fee_per_km (
    id character varying(20) NOT NULL,
    province character varying(25) NOT NULL,
    motorfee integer NOT NULL,
    carfee integer NOT NULL
);


ALTER TABLE sirest.delivery_fee_per_km OWNER TO db22a008;

--
-- Name: food; Type: TABLE; Schema: sirest; Owner: db22a008
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


ALTER TABLE sirest.food OWNER TO db22a008;

--
-- Name: food_category; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.food_category (
    id character varying(20) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE sirest.food_category OWNER TO db22a008;

--
-- Name: food_ingredient; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.food_ingredient (
    rname character varying(25) NOT NULL,
    rbranch character varying(25) NOT NULL,
    foodname character varying(50) NOT NULL,
    ingredient character varying(25) NOT NULL
);


ALTER TABLE sirest.food_ingredient OWNER TO db22a008;

--
-- Name: ingredient; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.ingredient (
    id character varying(25) NOT NULL,
    name character varying(25) NOT NULL
);


ALTER TABLE sirest.ingredient OWNER TO db22a008;

--
-- Name: min_transaction_promo; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.min_transaction_promo (
    id character varying(25) NOT NULL,
    minimumtransactionnum integer NOT NULL
);


ALTER TABLE sirest.min_transaction_promo OWNER TO db22a008;

--
-- Name: payment_method; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.payment_method (
    id character varying(25) NOT NULL,
    name character varying(25) NOT NULL
);


ALTER TABLE sirest.payment_method OWNER TO db22a008;

--
-- Name: payment_status; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.payment_status (
    id character varying(25) NOT NULL,
    name character varying(25) NOT NULL
);


ALTER TABLE sirest.payment_status OWNER TO db22a008;

--
-- Name: promo; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.promo (
    id character varying(25) NOT NULL,
    promoname character varying(25) NOT NULL,
    discount integer NOT NULL,
    CONSTRAINT valid_discount CHECK (((discount >= 1) AND (discount <= 100)))
);


ALTER TABLE sirest.promo OWNER TO db22a008;

--
-- Name: restaurant; Type: TABLE; Schema: sirest; Owner: db22a008
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
    rcategory character varying(20) NOT NULL,
    CONSTRAINT valid_rating CHECK (((rating >= 0) AND (rating <= 10)))
);


ALTER TABLE sirest.restaurant OWNER TO db22a008;

--
-- Name: restaurant_category; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.restaurant_category (
    id character varying(20) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE sirest.restaurant_category OWNER TO db22a008;

--
-- Name: restaurant_operating_hours; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.restaurant_operating_hours (
    name character varying(25) NOT NULL,
    branch character varying(25) NOT NULL,
    day character varying(10) NOT NULL,
    starthours time without time zone NOT NULL,
    endhours time without time zone NOT NULL
);


ALTER TABLE sirest.restaurant_operating_hours OWNER TO db22a008;

--
-- Name: restaurant_promo; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.restaurant_promo (
    rname character varying(25) NOT NULL,
    rbranch character varying(25) NOT NULL,
    pid character varying(25) NOT NULL,
    starttime timestamp without time zone NOT NULL,
    endtime timestamp without time zone NOT NULL
);


ALTER TABLE sirest.restaurant_promo OWNER TO db22a008;

--
-- Name: special_day_promo; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.special_day_promo (
    id character varying(25) NOT NULL,
    date timestamp without time zone NOT NULL
);


ALTER TABLE sirest.special_day_promo OWNER TO db22a008;

--
-- Name: transaction; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.transaction (
    email character varying(50) NOT NULL,
    datetime timestamp without time zone NOT NULL,
    street character varying(30) NOT NULL,
    district character varying(30) NOT NULL,
    city character varying(25) NOT NULL,
    province character varying(25) NOT NULL,
    totalfood integer NOT NULL,
    totaldiscount double precision NOT NULL,
    deliveryfee double precision NOT NULL,
    totalprice double precision NOT NULL,
    rating integer NOT NULL,
    pmid character varying(25) NOT NULL,
    psid character varying(25) NOT NULL,
    dfid character varying(20) NOT NULL,
    courierid character varying(50) NOT NULL
);


ALTER TABLE sirest.transaction OWNER TO db22a008;

--
-- Name: transaction_actor; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.transaction_actor (
    email character varying(50) NOT NULL,
    nik character varying(20) NOT NULL,
    bankname character varying(20) NOT NULL,
    accountno character varying(20) NOT NULL,
    restopay bigint DEFAULT 0 NOT NULL,
    adminid character varying(50) NOT NULL
);


ALTER TABLE sirest.transaction_actor OWNER TO db22a008;

--
-- Name: transaction_food; Type: TABLE; Schema: sirest; Owner: db22a008
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


ALTER TABLE sirest.transaction_food OWNER TO db22a008;

--
-- Name: transaction_history; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.transaction_history (
    email character varying(50) NOT NULL,
    datetime timestamp without time zone NOT NULL,
    tsid character varying(25) NOT NULL,
    datetimestatus character varying(20) NOT NULL
);


ALTER TABLE sirest.transaction_history OWNER TO db22a008;

--
-- Name: transaction_status; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.transaction_status (
    id character varying(25) NOT NULL,
    name character varying(25) NOT NULL
);


ALTER TABLE sirest.transaction_status OWNER TO db22a008;

--
-- Name: user_acc; Type: TABLE; Schema: sirest; Owner: db22a008
--

CREATE TABLE sirest.user_acc (
    email character varying(50) NOT NULL,
    password character varying(50) NOT NULL,
    phonenum character varying(20) NOT NULL,
    fname character varying(15) NOT NULL,
    lname character varying(15) NOT NULL
);


ALTER TABLE sirest.user_acc OWNER TO db22a008;

--
-- Data for Name: admin; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.admin (email) FROM stdin;
khazeley0@home.pl
bakerman1@creativecommons.org
gpicton2@theatlantic.com
aocahill3@cdbaby.com
rchamberlayne4@surveymonkey.com
\.


--
-- Data for Name: courier; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.courier (email, platenum, drivinglicensenum, vehicletype, vehiclebrand) FROM stdin;
rhotchkinp@wix.com      RQV0604 55367895.0      Hardtop MINI
dnairnsq@rambler.ru     EPV092  337865303.0     Hardtop MINI
slaightr@elegantthemes.com      7ZEE260 304098400.0     SUV     Acura
fcrutchers@fotki.com    4AQG261 501038069.0     Trucks  GMC
hcapinettit@cocolog-nifty.com   V625KS  519381116.0     Hatchback       Suzuki
gnice0@archive.org      EPV099  519381117.0     Hatchback       Suzuki
iborless1@soup.io       RPV098  519381118.0     Hatchback       Suzuki
dtammadge2@state.gov    EPV100  519381119.0     Hatchback       Suzuki
cschankelborg3@feedburner.com   RPV099  519381120.0     Hatchback       Suzuki
einsall4@goo.ne.jp      EPV101  519381121.0     Hatchback       Suzuki
\.


--
-- Data for Name: customer; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.customer (email, birthdate, sex) FROM stdin;
aendean5@shop-pro.jp    1991-11-16      F
shakonsen6@china.com.cn 1991-03-07      M
amaskall7@abc.net.au    1994-03-04      M
hgillion8@shutterfly.com        1998-03-31      F
jmatuszak9@technorati.com       1995-06-01      M
ospraberrya@clickbank.net       2001-07-28      F
smargramb@issuu.com     1993-11-21      M
aallowayc@wikimedia.org 1996-01-03      M
kochterlonied@php.net   2000-09-20      M
mknucklese@fda.gov      1999-03-29      F
rjobesf@hatena.ne.jp    1992-09-26      F
csnellingg@a8.net       1997-05-11      M
cmummeryh@taobao.com    1995-11-07      M
smenhcii@taobao.com     1996-01-06      M
gkeatj@merriam-webster.com      1991-12-02      F
moglassanek@nasa.gov    1997-01-27      M
mpunchardl@marketwatch.com      1994-05-10      F
coughtrightm@feedburner.com     1997-04-28      M
tgedneyn@networkadvertising.org 1992-08-04      M
pfairlamo@hp.com        1991-05-11      M
\.


--
-- Data for Name: delivery_fee_per_km; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.delivery_fee_per_km (id, province, motorfee, carfee) FROM stdin;
DFPK1   Jawa Timur      5000    10000
DFPK2   Jakarta 6000    11000
DFPK3   Sulawesi Barat  7000    12000
DFPK4   Sumatra Utara   8000    13000
DFPK5   Aceh    9000    14000
DFPK6   Papua Barat     10000   15000
DFPK7   Kalimantan Tengah       11000   16000
DFPK8   Sulawesi Tenggara       12000   17000
DFPK9   Jawa Barat      13000   18000
DFPK10  Bali    14000   19000
\.


--
-- Data for Name: food; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.food (rname, rbranch, foodname, description, stock, price, fcategory) FROM stdin;
Lynch-West      Stronghold      Chañar  Delicious & home made   50      20000   FC1
Windler-Herzog  Zoolab  Narrowleaf Evening Primrose     \N      14      21000   FC1
Ankunding-Bins  Tempsoft        Kahana Valley Cyrtandra \N      48      22000   FC1
Stehr-Murray    Vagram  Sugarberry      Fresh   84      23000   FC1
Runte-Walker    Overhold        Canyon Drymary  \N      39      24000   FC1
Wehner Inc      Tresom  Silky Lupine    Delicious & home made   31      25000   FC2
Champlin        Bigtax  Eclipta \N      43      26000   FC2
Witting Subin   Littlebrownjug  \N      97      27000   FC2
Sporer LLC      Span    Cutler's Jewelflower    Fresh   51      28000   FC2
Glover  Aerified        Dotted Lichen   Made with good ingredients      14      29000   FC2
Lynch-West      Stronghold      Shockley's Desert-thorn Made with good ingredients      93      30000   FC2
Windler-Herzog  Zoolab  Fourpoint Evening Primrose      \N      64      31000   FC3
Ankunding-Bins  Tempsoft        Lion's Heart    Delicious & home made   16      32000   FC3
Stehr-Murray    Vagram  Santa Fe Phlox  \N      56      33000   FC3
Runte-Walker    Overhold        Bush Monkeyflower       Fresh   61      34000   FC3
Wehner Inc      Tresom  Dore's Needlegrass      Fresh   22      35000   FC3
Champlin        Bigtax  Santa Rita Mountain Dodder      \N      34      36000   FC3
Witting Subin   Argentinian Crabgrass   \N      68      37000   FC4
Sporer LLC      Span    Slimspike Threeawn      \N      49      38000   FC4
Glover  Aerified        Prairie Fleabane        \N      85      39000   FC4
Lynch-West      Stronghold      Low Menodora    Delicious & home made   4       40000   FC4
Windler-Herzog  Zoolab  Nepalese Smartweed      \N      31      41000   FC4
Ankunding-Bins  Tempsoft        ohi'a Lehua     Delicious & home made   62      42000   FC4
Stehr-Murray    Vagram  Golden Sedge    Made with good ingredients      87      43000   FC5
Runte-Walker    Overhold        Manystem Liveforever    \N      94      44000   FC5
Wehner Inc      Tresom  Arthothelium Lichen     \N      96      45000   FC5
Champlin        Bigtax  Greene's Liveforever    Delicious       27      46000   FC5
Witting Subin   Pogonatum Moss  Made with good ingredients      99      47000   FC5
Sporer LLC      Span    Horseshoe Vetch \N      23      48000   FC5
Glover  Aerified        Reflexed Gyroweisia Moss        Delicious & home made   27      49000   FC5
\.


--
-- Data for Name: food_category; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.food_category (id, name) FROM stdin;
FC1     Pedas
FC2     Desert
FC3     Camilan
FC4     Junk Food
FC5     Healty
\.


--
-- Data for Name: food_ingredient; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.food_ingredient (rname, rbranch, foodname, ingredient) FROM stdin;
Lynch-West      Stronghold      Chañar  I2
Windler-Herzog  Zoolab  Narrowleaf Evening Primrose     I18
Ankunding-Bins  Tempsoft        Kahana Valley Cyrtandra I18
Stehr-Murray    Vagram  Sugarberry      I1
Runte-Walker    Overhold        Canyon Drymary  I7
Wehner Inc      Tresom  Silky Lupine    I9
Champlin        Bigtax  Eclipta I10
Witting Subin   Littlebrownjug  I11
Sporer LLC      Span    Cutler's Jewelflower    I12
Glover  Aerified        Dotted Lichen   I13
Lynch-West      Stronghold      Shockley's Desert-thorn I14
Windler-Herzog  Zoolab  Fourpoint Evening Primrose      I15
Ankunding-Bins  Tempsoft        Lion's Heart    I16
Stehr-Murray    Vagram  Santa Fe Phlox  I17
Runte-Walker    Overhold        Bush Monkeyflower       I18
Wehner Inc      Tresom  Dore's Needlegrass      I19
Champlin        Bigtax  Santa Rita Mountain Dodder      I20
Witting Subin   Argentinian Crabgrass   I19
Sporer LLC      Span    Slimspike Threeawn      I1
Glover  Aerified        Prairie Fleabane        I2
Lynch-West      Stronghold      Low Menodora    I3
Windler-Herzog  Zoolab  Nepalese Smartweed      I4
Ankunding-Bins  Tempsoft        ohi'a Lehua     I5
Stehr-Murray    Vagram  Golden Sedge    I6
Runte-Walker    Overhold        Manystem Liveforever    I7
Wehner Inc      Tresom  Arthothelium Lichen     I8
Champlin        Bigtax  Greene's Liveforever    I11
Witting Subin   Pogonatum Moss  I6
Sporer LLC      Span    Horseshoe Vetch I12
Glover  Aerified        Reflexed Gyroweisia Moss        I3
\.


--
-- Data for Name: ingredient; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.ingredient (id, name) FROM stdin;
I1      Bawang
I2      Tomat
I3      Garem
I4      Merica
I5      Kentang
I6      Ayam
I7      Daging
I8      Tempe
I9      Tahu
I10     Susu
I11     Santan
I12     Cabe
I13     Kerupuk
I14     Tepung
I15     Gula
I16     Madu
I17     Kecap
I18     Kedelai
I19     Sawi
I20     Kangkung
\.


--
-- Data for Name: min_transaction_promo; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.min_transaction_promo (id, minimumtransactionnum) FROM stdin;
P06     10
P07     20
P08     30
P09     40
P10     50
P11     60
P12     70
P13     80
P14     90
P15     100
\.


--
-- Data for Name: payment_method; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.payment_method (id, name) FROM stdin;
PM01    Transfer ATM
PM02    Transfer m-banking
PM03    Transfer Minimarket
PM04    Pembayaran RestoPay
PM05    Pembayaran e-wallet
\.


--
-- Data for Name: payment_status; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.payment_status (id, name) FROM stdin;
PS01    Menunggu Pembayaran
PS02    Berhasil
PS03    Gagal
\.


--
-- Data for Name: promo; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.promo (id, promoname, discount) FROM stdin;
P01     Promo Kemerdekaan       10
P02     Promo Lebaran   25
P03     Promo Natal     5
P04     Promo Waisak    5
P05     Promo Kurban    25
P06     Promo 10x       5
P07     Promo 20x       7
P08     Promo 30x       9
P09     Promo 40x       11
P10     Promo 50x       13
P11     Promo 60x       15
P12     Promo 70x       17
P13     Promo 80x       19
P14     Promo 90x       21
P15     Promo 100x      23
P16     Promo Valentine 11
P17     Promo goput     12
P18     Promo diesnatalis       13
P19     Promo Aniv      14
P20     Promo Wedding   15
\.


--
-- Data for Name: restaurant; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.restaurant (rname, rbranch, email, rphonenum, street, district, city, province, rating, rcategory) FROM stdin;
Lynch-West      Stronghold      lpowe5@flickr.com       9736788096.0    3 Elgar Parkway United States   Riverside       California      0       RC1
Windler-Herzog  Zoolab  mochterlony6@sina.com.cn        9713339306.0    31 Truax Street United States   Torrance        California      0       RC1
Ankunding-Bins  Tempsoft        mconiff7@mashable.com   4656581753.0    6 Bashford Center       United States   Honolulu        Hawaii  0       RC1
Stehr-Murray    Vagram  jketley8@dropbox.com    8349720256.0    726 Schmedeman Lane     United States   Clearwater      Florida 0       RC2
Runte-Walker    Overhold        khuxtable9@twitpic.com  8579413224.0    942 Cherokee Plaza      United States   Jacksonville    Florida 0       RC2
Wehner Inc      Tresom  aodeorana@clickbank.net 5267132937.0    771 Hanover Lane        United States   Los Angeles     California      0       RC2
Champlin        Bigtax  lcraneyb@dedecms.com    8476550475.0    7 Toban Lane    United States   Stockton        California      0       RC2
Witting Subin   jsidesc@linkedin.com    4436912535.0    4927 Maple Wood Avenue  United States   Orlando Florida 0       RC1
Sporer LLC      Span    fquelchd@simplemachines.org     6375809538.0    42 Hayes Drive  United States   Los Angeles     California      0       RC1
Glover  Aerified        ksweette@e-recht24.de   3154230958.0    3 Tony Pass     United States   Denver  Colorado        0       RC3
\.


--
-- Data for Name: restaurant_category; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.restaurant_category (id, name) FROM stdin;
RC1     Barat
RC2     Timur Tengah
RC3     Nusantara
RC4     Jepang
RC5     Korea
\.


--
-- Data for Name: restaurant_operating_hours; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.restaurant_operating_hours (name, branch, day, starthours, endhours) FROM stdin;
Lynch-West      Stronghold      Monday  08:18:00        21:08:00
Windler-Herzog  Zoolab  Monday  07:54:00        21:35:00
Ankunding-Bins  Tempsoft        Monday  09:07:00        22:04:00
Stehr-Murray    Vagram  Monday  07:52:00        21:39:00
Runte-Walker    Overhold        Monday  08:50:00        21:33:00
Wehner Inc      Tresom  Monday  09:40:00        21:09:00
Lynch-West      Stronghold      Tuesday 07:54:00        21:29:00
Windler-Herzog  Zoolab  Tuesday 09:49:00        22:28:00
Ankunding-Bins  Tempsoft        Tuesday 07:46:00        22:32:00
Stehr-Murray    Vagram  Tuesday 09:37:00        22:51:00
Runte-Walker    Overhold        Tuesday 08:16:00        22:47:00
Wehner Inc      Tresom  Tuesday 09:18:00        21:11:00
Lynch-West      Stronghold      Wednesday       07:55:00        21:10:00
Windler-Herzog  Zoolab  Wednesday       09:34:00        22:45:00
Ankunding-Bins  Tempsoft        Wednesday       09:31:00        22:35:00
Stehr-Murray    Vagram  Wednesday       09:16:00        21:57:00
Runte-Walker    Overhold        Wednesday       08:20:00        21:46:00
Wehner Inc      Tresom  Wednesday       07:45:00        21:36:00
Champlin        Bigtax  Wednesday       09:57:00        22:24:00
Lynch-West      Stronghold      Thursday        09:34:00        22:16:00
Windler-Herzog  Zoolab  Thursday        09:55:00        22:10:00
Ankunding-Bins  Tempsoft        Thursday        07:27:00        21:44:00
Stehr-Murray    Vagram  Thursday        08:05:00        21:17:00
Runte-Walker    Overhold        Thursday        09:38:00        22:36:00
Lynch-West      Stronghold      Friday  07:11:00        21:34:00
Windler-Herzog  Zoolab  Friday  07:05:00        22:40:00
Ankunding-Bins  Tempsoft        Friday  09:59:00        21:58:00
Stehr-Murray    Vagram  Friday  07:54:00        22:52:00
Runte-Walker    Overhold        Friday  08:14:00        22:54:00
Wehner Inc      Tresom  Friday  07:04:00        21:25:00
\.


--
-- Data for Name: restaurant_promo; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.restaurant_promo (rname, rbranch, pid, starttime, endtime) FROM stdin;
Lynch-West      Stronghold      P01     2022-01-01 00:00:00     2022-01-01 12:00:00
Windler-Herzog  Zoolab  P02     2022-05-04 20:00:00     2022-05-04 21:00:00
Ankunding-Bins  Tempsoft        P03     2022-02-03 01:00:00     2022-02-03 11:00:00
Stehr-Murray    Vagram  P04     2021-11-22 13:00:00     2021-11-22 15:00:00
Runte-Walker    Overhold        P05     2021-10-24 16:00:00     2021-10-24 17:00:00
Wehner Inc      Tresom  P06     2022-10-10 15:00:00     2022-10-10 15:30:00
Champlin        Bigtax  P07     2022-09-09 05:00:00     2022-09-09 09:00:00
Witting Subin   P08     2022-08-08 09:00:00     2022-08-08 12:00:00
Sporer LLC      Span    P09     2022-06-28 13:00:00     2022-06-28 14:00:00
Glover  Aerified        P10     2022-02-21 08:00:00     2022-02-21 20:00:00
\.


--
-- Data for Name: special_day_promo; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.special_day_promo (id, date) FROM stdin;
P01     2022-01-01 00:00:00
P02     2022-05-04 00:00:00
P03     2022-02-03 00:00:00
P04     2021-11-22 00:00:00
P05     2021-10-24 00:00:00
P16     2022-10-10 00:00:00
P17     2022-09-09 00:00:00
P18     2022-08-08 00:00:00
P19     2022-06-28 00:00:00
P20     2022-02-21 00:00:00
\.


--
-- Data for Name: transaction; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.transaction (email, datetime, street, district, city, province, totalfood, totaldiscount, deliveryfee, totalprice, rating, pmid, psid, dfid, courierid) FROM stdin;
aendean5@shop-pro.jp    2021-11-04 00:00:00     Hoffman 55441 Bonner Lane       Cleveland       Ohio    26      10      5000    59000   5       PM01    PS01DFPK1    rhotchkinp@wix.com
shakonsen6@china.com.cn 2022-06-05 00:00:00     Columbus        11 Beilfuss Avenue      New Haven       Connecticut     1       15      6000    58000   3   PM05     PS01    DFPK7   dnairnsq@rambler.ru
amaskall7@abc.net.au    2022-07-31 00:00:00     Parkside        8 Loftsgordon Alley     Memphis Tennessee       3       20      7000    57000   3       PM02PS03     DFPK3   slaightr@elegantthemes.com
hgillion8@shutterfly.com        2022-01-13 00:00:00     Golden Leaf     387 Mayer Park  Orange  California      2       25      8000    56000   5       PM03PS01     DFPK3   fcrutchers@fotki.com
jmatuszak9@technorati.com       2022-09-10 00:00:00     High Crossing   30 Spenser Drive        Long Beach      California      21      30      9000    550004       PM01    PS02    DFPK10  hcapinettit@cocolog-nifty.com
ospraberrya@clickbank.net       2022-09-14 00:00:00     Morningstar     95963 Loomis Pass       Abilene Texas   12      35      10000   54000   2       PM04PS02     DFPK6   gnice0@archive.org
smargramb@issuu.com     2021-12-01 00:00:00     Luster  057 Cascade Avenue      Boulder Colorado        30      40      11000   53000   3       PM04    PS01DFPK7    iborless1@soup.io
aallowayc@wikimedia.org 2021-12-17 00:00:00     Green Ridge     39 Pawling Trail        Washington      District of Columbia    10      45      12000   520004       PM05    PS03    DFPK8   dtammadge2@state.gov
kochterlonied@php.net   2022-09-27 00:00:00     Glacier Hill    53077 Mesta Trail       North Hollywood California      28      50      13000   51000   5   PM03     PS03    DFPK9   cschankelborg3@feedburner.com
mknucklese@fda.gov      2022-01-24 00:00:00     Mayer   1593 Leroy Road Toledo  Ohio    3       55      14000   50000   1       PM03    PS01    DFPK9   einsall4@goo.ne.jp
\.


--
-- Data for Name: transaction_actor; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.transaction_actor (email, nik, bankname, accountno, restopay, adminid) FROM stdin;
aendean5@shop-pro.jp    32750100001.0   BCA     1.0     0       khazeley0@home.pl
shakonsen6@china.com.cn 32750100002.0   BCA     2.0     0       khazeley0@home.pl
amaskall7@abc.net.au    32750100003.0   BCA     3.0     0       khazeley0@home.pl
hgillion8@shutterfly.com        32750100004.0   BCA     4.0     0       khazeley0@home.pl
jmatuszak9@technorati.com       32750100005.0   BCA     5.0     0       khazeley0@home.pl
ospraberrya@clickbank.net       32750100006.0   BCA     6.0     0       khazeley0@home.pl
smargramb@issuu.com     32750100007.0   BCA     7.0     0       bakerman1@creativecommons.org
aallowayc@wikimedia.org 32750100008.0   BCA     8.0     0       bakerman1@creativecommons.org
kochterlonied@php.net   32750100009.0   BCA     9.0     0       bakerman1@creativecommons.org
mknucklese@fda.gov      32750100010.0   BCA     10.0    0       bakerman1@creativecommons.org
rjobesf@hatena.ne.jp    32750100011.0   BCA     11.0    0       bakerman1@creativecommons.org
csnellingg@a8.net       32750100012.0   BCA     12.0    0       bakerman1@creativecommons.org
cmummeryh@taobao.com    32750100013.0   BCA     13.0    0       gpicton2@theatlantic.com
smenhcii@taobao.com     32750100014.0   BCA     14.0    0       gpicton2@theatlantic.com
gkeatj@merriam-webster.com      32750100015.0   BCA     15.0    0       gpicton2@theatlantic.com
moglassanek@nasa.gov    32750100016.0   BCA     16.0    0       gpicton2@theatlantic.com
mpunchardl@marketwatch.com      32750100017.0   BCA     17.0    0       aocahill3@cdbaby.com
coughtrightm@feedburner.com     32750100018.0   BCA     18.0    0       aocahill3@cdbaby.com
tgedneyn@networkadvertising.org 32750100019.0   BCA     19.0    0       aocahill3@cdbaby.com
pfairlamo@hp.com        32750100020.0   BCA     20.0    0       aocahill3@cdbaby.com
rhotchkinp@wix.com      32750100021.0   BCA     21.0    0       rchamberlayne4@surveymonkey.com
dnairnsq@rambler.ru     32750100022.0   BCA     22.0    0       rchamberlayne4@surveymonkey.com
slaightr@elegantthemes.com      32750100023.0   BCA     23.0    0       rchamberlayne4@surveymonkey.com
fcrutchers@fotki.com    32750100024.0   BCA     24.0    0       rchamberlayne4@surveymonkey.com
hcapinettit@cocolog-nifty.com   32750100025.0   BCA     25.0    0       rchamberlayne4@surveymonkey.com
gnice0@archive.org      32750100026.0   BCA     26.0    0       rchamberlayne4@surveymonkey.com
iborless1@soup.io       32750100027.0   BCA     27.0    0       rchamberlayne4@surveymonkey.com
dtammadge2@state.gov    32750100028.0   BCA     28.0    0       rchamberlayne4@surveymonkey.com
cschankelborg3@feedburner.com   32750100029.0   BCA     29.0    0       rchamberlayne4@surveymonkey.com
einsall4@goo.ne.jp      32750100030.0   BCA     30.0    0       rchamberlayne4@surveymonkey.com
lpowe5@flickr.com       32750100031.0   BCA     31.0    0       rchamberlayne4@surveymonkey.com
mochterlony6@sina.com.cn        32750100032.0   BCA     32.0    0       rchamberlayne4@surveymonkey.com
mconiff7@mashable.com   32750100033.0   BCA     33.0    0       rchamberlayne4@surveymonkey.com
jketley8@dropbox.com    32750100034.0   BCA     34.0    0       rchamberlayne4@surveymonkey.com
khuxtable9@twitpic.com  32750100035.0   BCA     35.0    0       rchamberlayne4@surveymonkey.com
aodeorana@clickbank.net 32750100036.0   BCA     36.0    0       rchamberlayne4@surveymonkey.com
lcraneyb@dedecms.com    32750100037.0   BCA     37.0    0       rchamberlayne4@surveymonkey.com
jsidesc@linkedin.com    32750100038.0   BCA     38.0    0       rchamberlayne4@surveymonkey.com
fquelchd@simplemachines.org     32750100039.0   BCA     39.0    0       rchamberlayne4@surveymonkey.com
ksweette@e-recht24.de   32750100040.0   BCA     40.0    0       rchamberlayne4@surveymonkey.com
\.


--
-- Data for Name: transaction_food; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.transaction_food (email, datetime, rname, rbranch, foodname, amount, note) FROM stdin;
aendean5@shop-pro.jp    2021-11-04 00:00:00     Lynch-West      Stronghold      Chañar  5       sukses
shakonsen6@china.com.cn 2022-06-05 00:00:00     Windler-Herzog  Zoolab  Narrowleaf Evening Primrose     5       sukses
amaskall7@abc.net.au    2022-07-31 00:00:00     Ankunding-Bins  Tempsoft        Kahana Valley Cyrtandra 5       sukses
hgillion8@shutterfly.com        2022-01-13 00:00:00     Stehr-Murray    Vagram  Sugarberry      5       sukses
jmatuszak9@technorati.com       2022-09-10 00:00:00     Runte-Walker    Overhold        Canyon Drymary  5       sukses
ospraberrya@clickbank.net       2022-09-14 00:00:00     Wehner Inc      Tresom  Silky Lupine    5       sukses
smargramb@issuu.com     2021-12-01 00:00:00     Champlin        Bigtax  Eclipta 5       sukses
aallowayc@wikimedia.org 2021-12-17 00:00:00     Witting Subin   Littlebrownjug  5       sukses
kochterlonied@php.net   2022-09-27 00:00:00     Sporer LLC      Span    Cutler's Jewelflower    5       sukses
mknucklese@fda.gov      2022-01-24 00:00:00     Glover  Aerified        Dotted Lichen   5       sukses
\.


--
-- Data for Name: transaction_history; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.transaction_history (email, datetime, tsid, datetimestatus) FROM stdin;
aendean5@shop-pro.jp    2021-11-04 00:00:00     TS04    Berhasil
shakonsen6@china.com.cn 2022-06-05 00:00:00     TS04    Berhasil
amaskall7@abc.net.au    2022-07-31 00:00:00     TS04    Berhasil
hgillion8@shutterfly.com        2022-01-13 00:00:00     TS04    Berhasil
jmatuszak9@technorati.com       2022-09-10 00:00:00     TS04    Berhasil
ospraberrya@clickbank.net       2022-09-14 00:00:00     TS04    Berhasil
smargramb@issuu.com     2021-12-01 00:00:00     TS04    Berhasil
aallowayc@wikimedia.org 2021-12-17 00:00:00     TS04    Berhasil
kochterlonied@php.net   2022-09-27 00:00:00     TS04    Berhasil
mknucklese@fda.gov      2022-01-24 00:00:00     TS04    Berhasil
\.


--
-- Data for Name: transaction_status; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.transaction_status (id, name) FROM stdin;
TS01    Menunggu Konfirmasi
TS02    Pesanan Dibuat
TS03    Pesanan Diantar
TS04    Pesanan Selesai
TS05    Pesanan Dibatalkan
\.


--
-- Data for Name: user_acc; Type: TABLE DATA; Schema: sirest; Owner: db22a008
--

COPY sirest.user_acc (email, password, phonenum, fname, lname) FROM stdin;
khazeley0@home.pl       gQ5Q4J  9797095170.0    Karlis  Hazeley
bakerman1@creativecommons.org   8m8tmXk 9435453327.0    Brigitta        Akerman
gpicton2@theatlantic.com        iVniGL2 7327591920.0    Gina    Picton
aocahill3@cdbaby.com    VRkOPTeO        8623579475.0    Alane   O'Cahill
rchamberlayne4@surveymonkey.com knsBcXOIH2P2    4185085201.0    Royall  Chamberlayne
aendean5@shop-pro.jp    C5dCTrK 3247924250.0    Aron    Endean
shakonsen6@china.com.cn ybvT7Ts6w       6343109284.0    Sabrina Hakonsen
amaskall7@abc.net.au    hcuz7ov 9269854511.0    Adrianna        Maskall
hgillion8@shutterfly.com        adJWJe  9318807454.0    Hunt    Gillion
jmatuszak9@technorati.com       tEMg8hj 7042024881.0    Jo      Matuszak
ospraberrya@clickbank.net       oHnvc5  2353467931.0    Odette  Spraberry
smargramb@issuu.com     l12x8O2S2U      9737035904.0    Steve   Margram
aallowayc@wikimedia.org pQ5GTldDyV      6109504607.0    Aurthur Alloway
kochterlonied@php.net   soLRNsWyN984    1901426289.0    Kendal  Ochterlonie
mknucklese@fda.gov      guI2is  8497050936.0    Melvyn  Knuckles
rjobesf@hatena.ne.jp    7l1te8gopliz    9796523676.0    Rollin  Jobes
csnellingg@a8.net       cSRRwnNzY       3908427222.0    Celinka Snelling
cmummeryh@taobao.com    Dx6AQegqK407    4584287682.0    Corey   Mummery
smenhcii@taobao.com     trxsyV0iFPMI    4771473521.0    Stanford        Menhci
gkeatj@merriam-webster.com      aENQaL6 5705072840.0    Griff   Keat
moglassanek@nasa.gov    rrAMZ1Xw0       3912983288.0    Mose    O'Glassane
mpunchardl@marketwatch.com      IzwmJGG 3716741686.0    Moira   Punchard
coughtrightm@feedburner.com     l54wKP  4598656492.0    Caroline        Oughtright
tgedneyn@networkadvertising.org QBt3RhCOr       8502257817.0    Theresa Gedney
pfairlamo@hp.com        8E4ovSDgzj      6139650832.0    Pryce   Fairlam
rhotchkinp@wix.com      wDj0p9a1qSV     8614575362.0    Rik     Hotchkin
dnairnsq@rambler.ru     vqQpNvdWN17     7786393521.0    Decca   Nairns
slaightr@elegantthemes.com      99AWwZ0CMX      7019983874.0    Sonni   Laight
fcrutchers@fotki.com    P3dVFtxF1C      9658755414.0    Floria  Crutcher
hcapinettit@cocolog-nifty.com   0aT0OuwkuL      1789048018.0    Hatti   Capinetti
gnice0@archive.org      ldLzlxalC       1726593971.0    Godiva  Nice
iborless1@soup.io       zyK3pW66A       6026297521.0    Ianthe  Borless
dtammadge2@state.gov    zMJBnVb 7889634452.0    Daphne  Tammadge
cschankelborg3@feedburner.com   MExPyENa        4179199197.0    Carlynne        Schankelborg
einsall4@goo.ne.jp      ogMAc6Q 2911663558.0    Early   Insall
lpowe5@flickr.com       smr6Otp5uz      6737626996.0    Laura   Powe
mochterlony6@sina.com.cn        2jqWh2  7796365953.0    Marlin  Ochterlony
mconiff7@mashable.com   J6R3cT2 3733470326.0    Madel   Coniff
jketley8@dropbox.com    lDDGiHG 2461203824.0    Joellen Ketley
khuxtable9@twitpic.com  2vK3Ef  9365678225.0    Kristoforo      Huxtable
aodeorana@clickbank.net X80n2n  9556143701.0    Antonia O'Deoran
lcraneyb@dedecms.com    XnmnuPs 5846135768.0    Luella  Craney
jsidesc@linkedin.com    C5duqNf 4972376001.0    Johnathan       Sides
fquelchd@simplemachines.org     KtNuzxT 1877644181.0    Filippa Quelch
ksweette@e-recht24.de   EOtOHpZtUq      1977208180.0    Kevan   Sweett
\.


--
-- Name: admin admin_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (email);


--
-- Name: courier courier_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.courier
    ADD CONSTRAINT courier_pkey PRIMARY KEY (email);


--
-- Name: customer customer_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (email);


--
-- Name: delivery_fee_per_km delivery_fee_per_km_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.delivery_fee_per_km
    ADD CONSTRAINT delivery_fee_per_km_pkey PRIMARY KEY (id);


--
-- Name: food_category food_category_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.food_category
    ADD CONSTRAINT food_category_pkey PRIMARY KEY (id);


--
-- Name: food_ingredient food_ingredient_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.food_ingredient
    ADD CONSTRAINT food_ingredient_pkey PRIMARY KEY (rname, rbranch, foodname, ingredient);


--
-- Name: food food_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.food
    ADD CONSTRAINT food_pkey PRIMARY KEY (rname, rbranch, foodname);


--
-- Name: ingredient ingredient_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.ingredient
    ADD CONSTRAINT ingredient_pkey PRIMARY KEY (id);


--
-- Name: min_transaction_promo min_transaction_promo_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.min_transaction_promo
    ADD CONSTRAINT min_transaction_promo_pkey PRIMARY KEY (id);


--
-- Name: payment_method payment_method_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.payment_method
    ADD CONSTRAINT payment_method_pkey PRIMARY KEY (id);


--
-- Name: payment_status payment_status_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.payment_status
    ADD CONSTRAINT payment_status_pkey PRIMARY KEY (id);


--
-- Name: promo promo_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.promo
    ADD CONSTRAINT promo_pkey PRIMARY KEY (id);


--
-- Name: restaurant_category restaurant_category_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.restaurant_category
    ADD CONSTRAINT restaurant_category_pkey PRIMARY KEY (id);


--
-- Name: restaurant_operating_hours restaurant_operating_hours_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.restaurant_operating_hours
    ADD CONSTRAINT restaurant_operating_hours_pkey PRIMARY KEY (name, branch, day);


--
-- Name: restaurant restaurant_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.restaurant
    ADD CONSTRAINT restaurant_pkey PRIMARY KEY (rname, rbranch);


--
-- Name: restaurant_promo restaurant_promo_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.restaurant_promo
    ADD CONSTRAINT restaurant_promo_pkey PRIMARY KEY (rname, rbranch, pid);


--
-- Name: special_day_promo special_day_promo_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.special_day_promo
    ADD CONSTRAINT special_day_promo_pkey PRIMARY KEY (id);


--
-- Name: transaction_actor transaction_actor_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.transaction_actor
    ADD CONSTRAINT transaction_actor_pkey PRIMARY KEY (email);


--
-- Name: transaction_food transaction_food_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.transaction_food
    ADD CONSTRAINT transaction_food_pkey PRIMARY KEY (email, datetime, rname, rbranch, foodname);


--
-- Name: transaction_history transaction_history_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.transaction_history
    ADD CONSTRAINT transaction_history_pkey PRIMARY KEY (email, datetime, tsid);


--
-- Name: transaction transaction_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.transaction
    ADD CONSTRAINT transaction_pkey PRIMARY KEY (email, datetime);


--
-- Name: transaction_status transaction_status_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.transaction_status
    ADD CONSTRAINT transaction_status_pkey PRIMARY KEY (id);


--
-- Name: user_acc user_acc_pkey; Type: CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.user_acc
    ADD CONSTRAINT user_acc_pkey PRIMARY KEY (email);


--
-- Name: user_acc check_password; Type: TRIGGER; Schema: sirest; Owner: db22a008
--

CREATE TRIGGER check_password BEFORE INSERT OR UPDATE ON sirest.user_acc FOR EACH ROW EXECUTE PROCEDURE sirest.check_password();


--
-- Name: transaction_actor check_saldo; Type: TRIGGER; Schema: sirest; Owner: db22a008
--

CREATE TRIGGER check_saldo BEFORE INSERT OR UPDATE ON sirest.transaction_actor FOR EACH ROW EXECUTE PROCEDURE sirest.check_saldo();


--
-- Name: special_day_promo date_promo_violation; Type: TRIGGER; Schema: sirest; Owner: db22a008
--

CREATE TRIGGER date_promo_violation BEFORE INSERT OR UPDATE OF date ON sirest.special_day_promo FOR EACH ROW EXECUTE PROCEDURE sirest.check_date_promo_violation();


--
-- Name: transaction_status menambah_restopay; Type: TRIGGER; Schema: sirest; Owner: db22a008
--

CREATE TRIGGER menambah_restopay AFTER UPDATE OF name ON sirest.transaction_status FOR EACH ROW EXECUTE PROCEDURE sirest.menambah_restopay();


--
-- Name: transaction total; Type: TRIGGER; Schema: sirest; Owner: db22a008
--

CREATE TRIGGER total BEFORE INSERT OR UPDATE ON sirest.transaction FOR EACH ROW EXECUTE PROCEDURE sirest.total();


--
-- Name: delivery_fee_per_km triggerbatasperkm; Type: TRIGGER; Schema: sirest; Owner: db22a008
--

CREATE TRIGGER triggerbatasperkm BEFORE INSERT OR UPDATE ON sirest.delivery_fee_per_km FOR EACH ROW EXECUTE PROCEDURE sirest.batasperkm();


--
-- Name: admin admin_email_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.admin
    ADD CONSTRAINT admin_email_fkey FOREIGN KEY (email) REFERENCES sirest.user_acc(email) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: courier courier_email_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.courier
    ADD CONSTRAINT courier_email_fkey FOREIGN KEY (email) REFERENCES sirest.transaction_actor(email) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: customer customer_email_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.customer
    ADD CONSTRAINT customer_email_fkey FOREIGN KEY (email) REFERENCES sirest.transaction_actor(email) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: food food_fcategory_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.food
    ADD CONSTRAINT food_fcategory_fkey FOREIGN KEY (fcategory) REFERENCES sirest.food_category(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: food_ingredient food_ingredient_ingredient_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.food_ingredient
    ADD CONSTRAINT food_ingredient_ingredient_fkey FOREIGN KEY (ingredient) REFERENCES sirest.ingredient(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: food_ingredient food_ingredient_rname_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.food_ingredient
    ADD CONSTRAINT food_ingredient_rname_fkey FOREIGN KEY (rname, rbranch, foodname) REFERENCES sirest.food(rname, rbranch, foodname) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: food food_rname_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.food
    ADD CONSTRAINT food_rname_fkey FOREIGN KEY (rname, rbranch) REFERENCES sirest.restaurant(rname, rbranch) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: min_transaction_promo min_transaction_promo_id_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.min_transaction_promo
    ADD CONSTRAINT min_transaction_promo_id_fkey FOREIGN KEY (id) REFERENCES sirest.promo(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: restaurant restaurant_email_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.restaurant
    ADD CONSTRAINT restaurant_email_fkey FOREIGN KEY (email) REFERENCES sirest.transaction_actor(email) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: restaurant_operating_hours restaurant_operating_hours_name_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.restaurant_operating_hours
    ADD CONSTRAINT restaurant_operating_hours_name_fkey FOREIGN KEY (name, branch) REFERENCES sirest.restaurant(rname, rbranch) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: restaurant_promo restaurant_promo_pid_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.restaurant_promo
    ADD CONSTRAINT restaurant_promo_pid_fkey FOREIGN KEY (pid) REFERENCES sirest.promo(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: restaurant_promo restaurant_promo_rname_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.restaurant_promo
    ADD CONSTRAINT restaurant_promo_rname_fkey FOREIGN KEY (rname, rbranch) REFERENCES sirest.restaurant(rname, rbranch);


--
-- Name: restaurant restaurant_rcategory_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.restaurant
    ADD CONSTRAINT restaurant_rcategory_fkey FOREIGN KEY (rcategory) REFERENCES sirest.restaurant_category(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: special_day_promo special_day_promo_id_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.special_day_promo
    ADD CONSTRAINT special_day_promo_id_fkey FOREIGN KEY (id) REFERENCES sirest.promo(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: transaction_actor transaction_actor_adminid_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.transaction_actor
    ADD CONSTRAINT transaction_actor_adminid_fkey FOREIGN KEY (adminid) REFERENCES sirest.admin(email) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: transaction_actor transaction_actor_email_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.transaction_actor
    ADD CONSTRAINT transaction_actor_email_fkey FOREIGN KEY (email) REFERENCES sirest.user_acc(email) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: transaction transaction_courierid_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.transaction
    ADD CONSTRAINT transaction_courierid_fkey FOREIGN KEY (courierid) REFERENCES sirest.courier(email) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: transaction transaction_dfid_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.transaction
    ADD CONSTRAINT transaction_dfid_fkey FOREIGN KEY (dfid) REFERENCES sirest.delivery_fee_per_km(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: transaction transaction_email_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.transaction
    ADD CONSTRAINT transaction_email_fkey FOREIGN KEY (email) REFERENCES sirest.customer(email) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: transaction_food transaction_food_email_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.transaction_food
    ADD CONSTRAINT transaction_food_email_fkey FOREIGN KEY (email, datetime) REFERENCES sirest.transaction(email, datetime) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: transaction_food transaction_food_rname_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.transaction_food
    ADD CONSTRAINT transaction_food_rname_fkey FOREIGN KEY (rname, rbranch, foodname) REFERENCES sirest.food(rname, rbranch, foodname) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: transaction_history transaction_history_email_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.transaction_history
    ADD CONSTRAINT transaction_history_email_fkey FOREIGN KEY (email, datetime) REFERENCES sirest.transaction(email, datetime) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: transaction_history transaction_history_tsid_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.transaction_history
    ADD CONSTRAINT transaction_history_tsid_fkey FOREIGN KEY (tsid) REFERENCES sirest.transaction_status(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: transaction transaction_pmid_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.transaction
    ADD CONSTRAINT transaction_pmid_fkey FOREIGN KEY (pmid) REFERENCES sirest.payment_method(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: transaction transaction_psid_fkey; Type: FK CONSTRAINT; Schema: sirest; Owner: db22a008
--

ALTER TABLE ONLY sirest.transaction
    ADD CONSTRAINT transaction_psid_fkey FOREIGN KEY (psid) REFERENCES sirest.payment_status(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

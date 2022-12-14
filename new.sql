CREATE TABLE admin (
    email character varying(50) NOT NULL
);

CREATE TABLE courier (
    email character varying(50) NOT NULL,
    platenum character varying(10) NOT NULL,
    drivinglicensenum character varying(20) NOT NULL,
    vehicletype character varying(15) NOT NULL,
    vehiclebrand character varying(15) NOT NULL
);

CREATE TABLE customer (
    email character varying(50) NOT NULL,
    birthdate date NOT NULL,
    sex character(1) NOT NULL
);

CREATE TABLE delivery_fee_per_km (
    id character varying(20) NOT NULL,
    province character varying(25) NOT NULL,
    motorfee integer NOT NULL,
    carfee integer NOT NULL
);

CREATE TABLE food (
    rname character varying(25) NOT NULL,
    rbranch character varying(25) NOT NULL,
    foodname character varying(50) NOT NULL,
    description text,
    stock integer NOT NULL,
    price bigint NOT NULL,
    fcategory character varying(20) NOT NULL
);

CREATE TABLE food_category (
    id character varying(20) NOT NULL,
    name character varying(50) NOT NULL
);

CREATE TABLE food_ingredient (
    rname character varying(25) NOT NULL,
    rbranch character varying(25) NOT NULL,
    foodname character varying(50) NOT NULL,
    ingredient character varying(25) NOT NULL
);

CREATE TABLE ingredient (
    id character varying(25) NOT NULL,
    name character varying(25) NOT NULL
);

CREATE TABLE min_transaction_promo (
    id character varying(25) NOT NULL,
    minimumtransactionnum integer NOT NULL
);

CREATE TABLE payment_method (
    id character varying(25) NOT NULL,
    name character varying(25) NOT NULL
);

CREATE TABLE payment_status (
    id character varying(25) NOT NULL,
    name character varying(25) NOT NULL
);

CREATE TABLE promo (
    id character varying(25) NOT NULL,
    promoname character varying(25) NOT NULL,
    discount integer NOT NULL,
    CONSTRAINT valid_discount CHECK (((discount >= 1) AND (discount <= 100)))
);

CREATE TABLE restaurant (
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

CREATE TABLE restaurant_category (
    id character varying(20) NOT NULL,
    name character varying(50) NOT NULL
);

CREATE TABLE restaurant_operating_hours (
    name character varying(25) NOT NULL,
    branch character varying(25) NOT NULL,
    day character varying(10) NOT NULL,
    starthours time without time zone NOT NULL,
    endhours time without time zone NOT NULL
);

CREATE TABLE restaurant_promo (
    rname character varying(25) NOT NULL,
    rbranch character varying(25) NOT NULL,
    pid character varying(25) NOT NULL,
    starttime timestamp without time zone NOT NULL,
    endtime timestamp without time zone NOT NULL
);

CREATE TABLE special_day_promo (
    id character varying(25) NOT NULL,
    date timestamp without time zone NOT NULL
);

CREATE TABLE transaction (
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

CREATE TABLE transaction_actor (
    email character varying(50) NOT NULL,
    nik character varying(20) NOT NULL,
    bankname character varying(20) NOT NULL,
    accountno character varying(20) NOT NULL,
    restopay bigint DEFAULT 0 NOT NULL,
    adminid character varying(50)
);

CREATE TABLE transaction_food (
    email character varying(50) NOT NULL,
    datetime timestamp without time zone NOT NULL,
    rname character varying(50) NOT NULL,
    rbranch character varying(25) NOT NULL,
    foodname character varying(50) NOT NULL,
    amount integer NOT NULL,
    note character varying(255)
);

CREATE TABLE transaction_history (
    email character varying(50) NOT NULL,
    datetime timestamp without time zone NOT NULL,
    tsid character varying(25) NOT NULL,
    datetimestatus character varying(20) NOT NULL
);

CREATE TABLE transaction_status (
    id character varying(25) NOT NULL,
    name character varying(25) NOT NULL
);

CREATE TABLE user_acc (
    email character varying(50) NOT NULL,
    password character varying(50) NOT NULL,
    phonenum character varying(20) NOT NULL,
    fname character varying(15) NOT NULL,
    lname character varying(15) NOT NULL
);

ALTER TABLE ONLY admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (email);

ALTER TABLE ONLY courier
    ADD CONSTRAINT courier_pkey PRIMARY KEY (email);

ALTER TABLE ONLY customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (email);

ALTER TABLE ONLY delivery_fee_per_km
    ADD CONSTRAINT delivery_fee_per_km_pkey PRIMARY KEY (id);

ALTER TABLE ONLY food_category
    ADD CONSTRAINT food_category_pkey PRIMARY KEY (id);

ALTER TABLE ONLY food_ingredient
    ADD CONSTRAINT food_ingredient_pkey PRIMARY KEY (rname, rbranch, foodname, ingredient);

ALTER TABLE ONLY food
    ADD CONSTRAINT food_pkey PRIMARY KEY (rname, rbranch, foodname);

ALTER TABLE ONLY ingredient
    ADD CONSTRAINT ingredient_pkey PRIMARY KEY (id);

ALTER TABLE ONLY min_transaction_promo
    ADD CONSTRAINT min_transaction_promo_pkey PRIMARY KEY (id);

ALTER TABLE ONLY payment_method
    ADD CONSTRAINT payment_method_pkey PRIMARY KEY (id);

ALTER TABLE ONLY payment_status
    ADD CONSTRAINT payment_status_pkey PRIMARY KEY (id);

ALTER TABLE ONLY promo
    ADD CONSTRAINT promo_pkey PRIMARY KEY (id);


ALTER TABLE ONLY restaurant_category
    ADD CONSTRAINT restaurant_category_pkey PRIMARY KEY (id);

ALTER TABLE ONLY restaurant_operating_hours
    ADD CONSTRAINT restaurant_operating_hours_pkey PRIMARY KEY (name, branch, day);

ALTER TABLE ONLY restaurant
    ADD CONSTRAINT restaurant_pkey PRIMARY KEY (rname, rbranch);

ALTER TABLE ONLY restaurant_promo
    ADD CONSTRAINT restaurant_promo_pkey PRIMARY KEY (rname, rbranch, pid);

ALTER TABLE ONLY special_day_promo
    ADD CONSTRAINT special_day_promo_pkey PRIMARY KEY (id);

ALTER TABLE ONLY transaction_actor
    ADD CONSTRAINT transaction_actor_pkey PRIMARY KEY (email);

ALTER TABLE ONLY transaction_food
    ADD CONSTRAINT transaction_food_pkey PRIMARY KEY (email, datetime, rname, rbranch, foodname);

ALTER TABLE ONLY transaction_history
    ADD CONSTRAINT transaction_history_pkey PRIMARY KEY (email, datetime, tsid);

ALTER TABLE ONLY transaction
    ADD CONSTRAINT transaction_pkey PRIMARY KEY (email, datetime);

ALTER TABLE ONLY transaction_status
    ADD CONSTRAINT transaction_status_pkey PRIMARY KEY (id);

ALTER TABLE ONLY user_acc
    ADD CONSTRAINT user_acc_pkey PRIMARY KEY (email);

ALTER TABLE ONLY admin
    ADD CONSTRAINT admin_email_fkey FOREIGN KEY (email) REFERENCES user_acc(email) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY courier
    ADD CONSTRAINT courier_email_fkey FOREIGN KEY (email) REFERENCES transaction_actor(email) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY customer
    ADD CONSTRAINT customer_email_fkey FOREIGN KEY (email) REFERENCES transaction_actor(email) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY food
    ADD CONSTRAINT food_fcategory_fkey FOREIGN KEY (fcategory) REFERENCES food_category(id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE ONLY food_ingredient
    ADD CONSTRAINT food_ingredient_ingredient_fkey FOREIGN KEY (ingredient) REFERENCES ingredient(id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE ONLY food_ingredient
    ADD CONSTRAINT food_ingredient_rname_fkey FOREIGN KEY (rname, rbranch, foodname) REFERENCES food(rname, rbranch, foodname) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY food
    ADD CONSTRAINT food_rname_fkey FOREIGN KEY (rname, rbranch) REFERENCES restaurant(rname, rbranch) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY min_transaction_promo
    ADD CONSTRAINT min_transaction_promo_id_fkey FOREIGN KEY (id) REFERENCES promo(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY restaurant
    ADD CONSTRAINT restaurant_email_fkey FOREIGN KEY (email) REFERENCES transaction_actor(email) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE ONLY restaurant_operating_hours
    ADD CONSTRAINT restaurant_operating_hours_name_fkey FOREIGN KEY (name, branch) REFERENCES restaurant(rname, rbranch) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY restaurant_promo
    ADD CONSTRAINT restaurant_promo_pid_fkey FOREIGN KEY (pid) REFERENCES promo(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY restaurant_promo
    ADD CONSTRAINT restaurant_promo_rname_fkey FOREIGN KEY (rname, rbranch) REFERENCES restaurant(rname, rbranch);

ALTER TABLE ONLY restaurant
    ADD CONSTRAINT restaurant_rcategory_fkey FOREIGN KEY (rcategory) REFERENCES restaurant_category(id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE ONLY special_day_promo
    ADD CONSTRAINT special_day_promo_id_fkey FOREIGN KEY (id) REFERENCES promo(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY transaction_actor
    ADD CONSTRAINT transaction_actor_adminid_fkey FOREIGN KEY (adminid) REFERENCES admin(email) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE ONLY transaction_actor
    ADD CONSTRAINT transaction_actor_email_fkey FOREIGN KEY (email) REFERENCES user_acc(email) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY transaction
    ADD CONSTRAINT transaction_courierid_fkey FOREIGN KEY (courierid) REFERENCES courier(email) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE ONLY transaction
    ADD CONSTRAINT transaction_dfid_fkey FOREIGN KEY (dfid) REFERENCES delivery_fee_per_km(id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE ONLY transaction
    ADD CONSTRAINT transaction_email_fkey FOREIGN KEY (email) REFERENCES customer(email) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY transaction_food
    ADD CONSTRAINT transaction_food_email_fkey FOREIGN KEY (email, datetime) REFERENCES transaction(email, datetime) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY transaction_food
    ADD CONSTRAINT transaction_food_rname_fkey FOREIGN KEY (rname, rbranch, foodname) REFERENCES food(rname, rbranch, foodname) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY transaction_history
    ADD CONSTRAINT transaction_history_email_fkey FOREIGN KEY (email, datetime) REFERENCES transaction(email, datetime) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY transaction_history
    ADD CONSTRAINT transaction_history_tsid_fkey FOREIGN KEY (tsid) REFERENCES transaction_status(id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE ONLY transaction
    ADD CONSTRAINT transaction_pmid_fkey FOREIGN KEY (pmid) REFERENCES payment_method(id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE ONLY transaction
    ADD CONSTRAINT transaction_psid_fkey FOREIGN KEY (psid) REFERENCES payment_status(id) ON UPDATE CASCADE ON DELETE RESTRICT;

CREATE FUNCTION batasperkm() RETURNS trigger
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

CREATE OR REPLACE FUNCTION check_date_promo_violation() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
SELECT RP.Starttime, RP.Endtime
FROM RESTAURANT_PROMO RP
WHERE RP.PId = NEW.Id;
IF (NEW.Date < RP.Starttime OR NEW.Date > RP.Endtime) THEN
RAISE EXCEPTION 'Maaf, promo tidak dapat diterapkan. Silakan masukkan tanggal yang valid!';
END IF;
RETURN NEW;
END IF;
END;
$$;

CREATE FUNCTION check_password() RETURNS trigger
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

CREATE FUNCTION check_saldo() RETURNS trigger
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

CREATE FUNCTION menambah_restopay() RETURNS trigger
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

CREATE FUNCTION total() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
 DECLARE
        TOTAL_BIAYA INT;
 BEGIN

  TOTAL_BIAYA = (total_makanan_harga-total_diskon) +biaya_pengantaran;
  RETURN NEW;
 END;
$$;

CREATE TRIGGER check_password BEFORE INSERT OR UPDATE ON user_acc FOR EACH ROW EXECUTE PROCEDURE check_password();

CREATE TRIGGER check_saldo BEFORE INSERT OR UPDATE ON transaction_actor FOR EACH ROW EXECUTE PROCEDURE check_saldo();

CREATE TRIGGER date_promo_violation BEFORE INSERT OR UPDATE OF date ON special_day_promo FOR EACH ROW EXECUTE PROCEDURE check_date_promo_violation();

CREATE TRIGGER menambah_restopay AFTER UPDATE OF name ON transaction_status FOR EACH ROW EXECUTE PROCEDURE menambah_restopay();

CREATE TRIGGER total BEFORE INSERT OR UPDATE ON transaction FOR EACH ROW EXECUTE PROCEDURE total();

CREATE TRIGGER triggerbatasperkm BEFORE INSERT OR UPDATE ON delivery_fee_per_km FOR EACH ROW EXECUTE PROCEDURE batasperkm();

INSERT INTO RESTAURANT_CATEGORY VALUES
    ('RC1','Barat'),
    ('RC2','Timur Tengah'),
    ('RC3','Nusantara'),
    ('RC4','Jepang'),
    ('RC5','Korea');

INSERT INTO FOOD_CATEGORY VALUES
    ('FC1','Pedas'),
    ('FC2','Desert'),
    ('FC3','Camilan'),
    ('FC4','Junk Food'),
    ('FC5','Healty');

INSERT INTO INGREDIENT VALUES
    ('I1','Bawang'),
    ('I2','Tomat'),
    ('I3','Garem'),
    ('I4','Merica'),
    ('I5','Kentang'),
    ('I6','Ayam'),
    ('I7','Daging'),
    ('I8','Tempe'),
    ('I9','Tahu'),
    ('I10','Susu'),
    ('I11','Santan'),
    ('I12','Cabe'),
    ('I13','Kerupuk'),
    ('I14','Tepung'),
    ('I15','Gula'),
    ('I16','Madu'),
    ('I17','Kecap'),
    ('I18','Kedelai'),
    ('I19','Sawi'),
    ('I20','Kangkung');

INSERT INTO DELIVERY_FEE_PER_KM VALUES
    ('DFPK1','Jawa Timur',5000.0,7000.0),
    ('DFPK2','Jakarta',6000.0,7000.0),
    ('DFPK3','Sulawesi Barat',6000.0,7000.0),
    ('DFPK4','Sumatra Utara',6000.0,7000.0),
    ('DFPK5','Aceh',6000.0,7000.0),
    ('DFPK6','Papua Barat',6000.0,7000.0),
    ('DFPK7','Kalimantan Tengah',5000.0,7000.0),
    ('DFPK8','Sulawesi Tenggara',5000.0,7000.0),
    ('DFPK9','Jawa Barat',5000.0,7000.0),
    ('DFPK10','Bali',5000.0,7000.0);

INSERT INTO PAYMENT_METHOD VALUES
    ('PM01','Transfer ATM'),
    ('PM02','Transfer m-banking'),
    ('PM03','Transfer Minimarket'),
    ('PM04','Pembayaran RestoPay'),
    ('PM05','Pembayaran e-wallet');

INSERT INTO PAYMENT_STATUS VALUES
    ('PS01','Menunggu Pembayaran'),
    ('PS02','Berhasil'),
    ('PS03','Gagal');

INSERT INTO TRANSACTION_STATUS VALUES
    ('TS01','Menunggu Konfirmasi'),
    ('TS02','Pesanan Dibuat'),
    ('TS03','Pesanan Diantar'),
    ('TS04','Pesanan Selesai'),
    ('TS05','Pesanan Dibatalkan');

INSERT INTO PROMO VALUES
    ('P01','Promo Kemerdekaan',10.0),
    ('P02','Promo Lebaran',25.0),
    ('P03','Promo Natal',5.0),
    ('P04','Promo Waisak',5.0),
    ('P05','Promo Kurban',25.0),
    ('P06','Promo 10x',5.0),
    ('P07','Promo 20x',7.0),
    ('P08','Promo 30x',9.0),
    ('P09','Promo 40x',11.0),
    ('P10','Promo 50x',13.0),
    ('P11','Promo 60x',15.0),
    ('P12','Promo 70x',17.0),
    ('P13','Promo 80x',19.0),
    ('P14','Promo 90x',21.0),
    ('P15','Promo 100x',23.0),
    ('P16','Promo Valentine',11.0),
    ('P17','Promo goput',12.0),
    ('P18','Promo diesnatalis',13.0),
    ('P19','Promo Aniv',14.0),
    ('P20','Promo Wedding',15.0);

INSERT INTO MIN_TRANSACTION_PROMO VALUES
    ('P06',10.0),
    ('P07',20.0),
    ('P08',30.0),
    ('P09',40.0),
    ('P10',50.0),
    ('P11',60.0),
    ('P12',70.0),
    ('P13',80.0),
    ('P14',90.0),
    ('P15',100.0);
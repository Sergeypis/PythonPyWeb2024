PGDMP      ;            	    |         	   DevDB2024    16.4    16.4 9    W           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            X           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            Y           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            Z           1262    16397 	   DevDB2024    DATABASE        CREATE DATABASE "DevDB2024" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE "DevDB2024";
                postgres    false                        2615    16468    Cars    SCHEMA        CREATE SCHEMA "Cars";
    DROP SCHEMA "Cars";
                postgres    false                        2615    16469    Clients    SCHEMA        CREATE SCHEMA "Clients";
    DROP SCHEMA "Clients";
                postgres    false                        2615    16467 
   Operations    SCHEMA        CREATE SCHEMA "Operations";
    DROP SCHEMA "Operations";
                postgres    false            �            1259    16569    Vehicle    TABLE     1  CREATE TABLE "Cars"."Vehicle" (
    vin character varying(17) NOT NULL,
    model character varying(30) NOT NULL,
    number_plate character varying(12) NOT NULL,
    year_of_manufacture integer NOT NULL,
    number_of_seats integer NOT NULL,
    type character varying(30) DEFAULT 'not set'::text,
    fuel_type character varying(30),
    resource integer NOT NULL,
    mileage integer NOT NULL,
    decommissioned boolean DEFAULT false,
    CONSTRAINT ch_car_resource CHECK (((resource >= 0) AND (resource < 20))),
    CONSTRAINT ch_mileage CHECK ((mileage >= 0)),
    CONSTRAINT ch_num_plate CHECK (((number_plate)::text ~ '(?:^[АВЕКМНОРСТУХ]\d{3}(?<!000)[АВЕКМНОРСТУХ]{2}\d{2,3}RUS$)|(?:^[АВЕКМНОРСТУХ]{2}\d{3}(?<!000)\d{2,3}RUS$)'::text)),
    CONSTRAINT ch_num_seats CHECK (((number_of_seats >= 0) AND (number_of_seats <= 100))),
    CONSTRAINT ch_vin CHECK (((vin)::text <> ''::text)),
    CONSTRAINT ch_year_vehicle CHECK (((year_of_manufacture > 1900) AND (year_of_manufacture <= (date_part('year'::text, now()))::integer)))
);
    DROP TABLE "Cars"."Vehicle";
       Cars         heap    postgres    false    7            �            1259    16561    Vehicle_type    TABLE     A  CREATE TABLE "Cars"."Vehicle_type" (
    type character varying(30) NOT NULL,
    max_allowed_speed integer DEFAULT 70,
    CONSTRAINT "Vehicle_type_max_allowed_speed_check" CHECK (((max_allowed_speed >= 40) AND (max_allowed_speed <= 130))),
    CONSTRAINT "Vehicle_type_type_check" CHECK (((type)::text <> ''::text))
);
 "   DROP TABLE "Cars"."Vehicle_type";
       Cars         heap    postgres    false    7            �            1259    16597 	   Passenger    TABLE       CREATE TABLE "Clients"."Passenger" (
    pass_id integer NOT NULL,
    lastname character varying(30) NOT NULL,
    firstname character varying(30) NOT NULL,
    patronymic character varying(30),
    passport character(12) NOT NULL,
    birthday date NOT NULL,
    CONSTRAINT "Passenger_lastname_check" CHECK (((lastname)::text <> ''::text)),
    CONSTRAINT "Passenger_lastname_check1" CHECK (((lastname)::text <> ''::text)),
    CONSTRAINT "Passenger_passport_check" CHECK ((passport ~ '(?:^\d{2}\s\d{2}\s)(?:\d{6})'::text))
);
 "   DROP TABLE "Clients"."Passenger";
       Clients         heap    postgres    false    8            �            1259    16596    Passenger_pass_id_seq    SEQUENCE     �   ALTER TABLE "Clients"."Passenger" ALTER COLUMN pass_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "Clients"."Passenger_pass_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            Clients          postgres    false    225    8            �            1259    16633    Ticket    TABLE     q  CREATE TABLE "Clients"."Ticket" (
    ticked_id integer NOT NULL,
    schedule_id integer NOT NULL,
    pass_id integer NOT NULL,
    cost money DEFAULT (0.00)::money NOT NULL,
    place_number integer,
    CONSTRAINT "Ticket_cost_check" CHECK ((cost >= (0)::money)),
    CONSTRAINT "Ticket_place_number_check" CHECK (((place_number > 0) AND (place_number <= 100)))
);
    DROP TABLE "Clients"."Ticket";
       Clients         heap    postgres    false    8            �            1259    16632    Ticket_ticked_id_seq    SEQUENCE     �   ALTER TABLE "Clients"."Ticket" ALTER COLUMN ticked_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "Clients"."Ticket_ticked_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            Clients          postgres    false    8    229            �            1259    16548    Driver    TABLE       CREATE TABLE "Operations"."Driver" (
    driver_id integer NOT NULL,
    lastname character varying(30) NOT NULL,
    firstname character varying(30) NOT NULL,
    patronymic character varying(30),
    passport character(12) NOT NULL,
    birthday date NOT NULL,
    date_of_employment date NOT NULL,
    drivers_license character(12) NOT NULL,
    drivers_license_category character varying(30) NOT NULL,
    date_of_issue_license date NOT NULL,
    CONSTRAINT "Driver_drivers_license_category_check" CHECK (((drivers_license_category)::text ~ '^(?:A|B|C|D|E|M|BE|CE|DE|C1|C1E|D1|D1E|Tm|Tb|A1|B1)(?:\s*,\s*(?:A|B|C|D|E|M|BE|CE|DE|C1|C1E|D1|D1E|Tm|Tb|A1|B1))*$'::text)),
    CONSTRAINT "Driver_drivers_license_check" CHECK ((drivers_license ~ '(^\d{2}\s\d{2}\s)(\d{6})'::text)),
    CONSTRAINT "Driver_lastname_check" CHECK (((lastname)::text <> ''::text)),
    CONSTRAINT "Driver_lastname_check1" CHECK (((lastname)::text <> ''::text)),
    CONSTRAINT "Driver_passport_check" CHECK ((passport ~ '(?:^\d{2}\s\d{2}\s)(?:\d{6})'::text))
);
 "   DROP TABLE "Operations"."Driver";
    
   Operations         heap    postgres    false    6            �            1259    16547    Driver_driver_id_seq    SEQUENCE     �   CREATE SEQUENCE "Operations"."Driver_driver_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE "Operations"."Driver_driver_id_seq";
    
   Operations          postgres    false    221    6            [           0    0    Driver_driver_id_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE "Operations"."Driver_driver_id_seq" OWNED BY "Operations"."Driver".driver_id;
       
   Operations          postgres    false    220            �            1259    16534    Route    TABLE     c  CREATE TABLE "Operations"."Route" (
    route_id integer NOT NULL,
    depart character varying(30) NOT NULL,
    arrive character varying(30) NOT NULL,
    distance integer NOT NULL,
    trip_time character varying(30) NOT NULL,
    active boolean DEFAULT true NOT NULL,
    CONSTRAINT "Route_arrive_check" CHECK (((arrive)::text <> ''::text)),
    CONSTRAINT "Route_depart_check" CHECK (((depart)::text <> ''::text)),
    CONSTRAINT "Route_distance_check" CHECK ((distance > 0)),
    CONSTRAINT route_trip_time_check CHECK (((trip_time)::text ~ '(?:\d\d?\s(?:days?)\s)?(?:[0-2]?[0-9]:[0-5][0-9])$'::text))
);
 !   DROP TABLE "Operations"."Route";
    
   Operations         heap    postgres    false    6            �            1259    16655    Long_routs_view    VIEW     �   CREATE VIEW "Operations"."Long_routs_view" AS
 SELECT depart,
    arrive,
    trip_time
   FROM "Operations"."Route"
  WHERE ((active IS TRUE) AND ((trip_time)::interval >= '1 day'::interval));
 *   DROP VIEW "Operations"."Long_routs_view";
    
   Operations          postgres    false    219    219    219    219    6            �            1259    16533    Route_route_id_seq    SEQUENCE     �   CREATE SEQUENCE "Operations"."Route_route_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE "Operations"."Route_route_id_seq";
    
   Operations          postgres    false    6    219            \           0    0    Route_route_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE "Operations"."Route_route_id_seq" OWNED BY "Operations"."Route".route_id;
       
   Operations          postgres    false    218            �            1259    16608    Schedule    TABLE     �  CREATE TABLE "Operations"."Schedule" (
    schedule_id integer NOT NULL,
    route_id integer NOT NULL,
    vin character varying(17) NOT NULL,
    date_depart date NOT NULL,
    time_depart time without time zone NOT NULL,
    driver_id integer,
    tickets_avaliable integer NOT NULL,
    CONSTRAINT "Schedule_tickets_avaliable_check" CHECK (((tickets_avaliable >= 0) AND (tickets_avaliable <= 100))),
    CONSTRAINT "Schedule_vin_check" CHECK (((vin)::text <> ''::text))
);
 $   DROP TABLE "Operations"."Schedule";
    
   Operations         heap    postgres    false    6            �            1259    16607    Schedule_chedule_id_seq    SEQUENCE     �   ALTER TABLE "Operations"."Schedule" ALTER COLUMN schedule_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "Operations"."Schedule_chedule_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
         
   Operations          postgres    false    227    6            �            1259    16659    Travel_info_view    VIEW     �  CREATE VIEW "Operations"."Travel_info_view" AS
 SELECT opr.depart AS "Пункт отправления",
    opr.arrive AS "Пункт назначения",
    cv.model AS "Модель ТС",
    cv.number_plate AS "Гос.номер",
    concat_ws(' '::text, od.lastname, od.firstname, od.patronymic) AS "ФИО Водителя",
    concat_ws(' '::text, cp.lastname, cp.firstname, cp.patronymic) AS "ФИО Пассажира",
    ct.place_number AS "№ места"
   FROM ((((("Clients"."Passenger" cp
     JOIN "Clients"."Ticket" ct ON ((cp.pass_id = ct.pass_id)))
     JOIN "Operations"."Schedule" os ON ((ct.schedule_id = os.schedule_id)))
     JOIN "Operations"."Route" opr ON ((os.route_id = opr.route_id)))
     JOIN "Cars"."Vehicle" cv ON (((os.vin)::text = (cv.vin)::text)))
     JOIN "Operations"."Driver" od ON ((os.driver_id = od.driver_id)))
  WHERE (os.date_depart >= now());
 +   DROP VIEW "Operations"."Travel_info_view";
    
   Operations          postgres    false    221    221    219    219    219    229    229    229    227    227    227    227    227    225    225    225    225    223    223    223    221    221    6            y           2604    16551    Driver driver_id    DEFAULT     �   ALTER TABLE ONLY "Operations"."Driver" ALTER COLUMN driver_id SET DEFAULT nextval('"Operations"."Driver_driver_id_seq"'::regclass);
 G   ALTER TABLE "Operations"."Driver" ALTER COLUMN driver_id DROP DEFAULT;
    
   Operations          postgres    false    221    220    221            w           2604    16537    Route route_id    DEFAULT     �   ALTER TABLE ONLY "Operations"."Route" ALTER COLUMN route_id SET DEFAULT nextval('"Operations"."Route_route_id_seq"'::regclass);
 E   ALTER TABLE "Operations"."Route" ALTER COLUMN route_id DROP DEFAULT;
    
   Operations          postgres    false    218    219    219            N          0    16569    Vehicle 
   TABLE DATA           �   COPY "Cars"."Vehicle" (vin, model, number_plate, year_of_manufacture, number_of_seats, type, fuel_type, resource, mileage, decommissioned) FROM stdin;
    Cars          postgres    false    223   8U       M          0    16561    Vehicle_type 
   TABLE DATA           A   COPY "Cars"."Vehicle_type" (type, max_allowed_speed) FROM stdin;
    Cars          postgres    false    222   V       P          0    16597 	   Passenger 
   TABLE DATA           f   COPY "Clients"."Passenger" (pass_id, lastname, firstname, patronymic, passport, birthday) FROM stdin;
    Clients          postgres    false    225   �V       T          0    16633    Ticket 
   TABLE DATA           Z   COPY "Clients"."Ticket" (ticked_id, schedule_id, pass_id, cost, place_number) FROM stdin;
    Clients          postgres    false    229   HX       L          0    16548    Driver 
   TABLE DATA           �   COPY "Operations"."Driver" (driver_id, lastname, firstname, patronymic, passport, birthday, date_of_employment, drivers_license, drivers_license_category, date_of_issue_license) FROM stdin;
 
   Operations          postgres    false    221   �X       J          0    16534    Route 
   TABLE DATA           ^   COPY "Operations"."Route" (route_id, depart, arrive, distance, trip_time, active) FROM stdin;
 
   Operations          postgres    false    219   wY       R          0    16608    Schedule 
   TABLE DATA           ~   COPY "Operations"."Schedule" (schedule_id, route_id, vin, date_depart, time_depart, driver_id, tickets_avaliable) FROM stdin;
 
   Operations          postgres    false    227   Z       ]           0    0    Passenger_pass_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('"Clients"."Passenger_pass_id_seq"', 10, true);
          Clients          postgres    false    224            ^           0    0    Ticket_ticked_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('"Clients"."Ticket_ticked_id_seq"', 7, true);
          Clients          postgres    false    228            _           0    0    Driver_driver_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('"Operations"."Driver_driver_id_seq"', 7, true);
       
   Operations          postgres    false    220            `           0    0    Route_route_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('"Operations"."Route_route_id_seq"', 7, true);
       
   Operations          postgres    false    218            a           0    0    Schedule_chedule_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('"Operations"."Schedule_chedule_id_seq"', 5, true);
       
   Operations          postgres    false    226            �           2606    16573    Vehicle Vehicle_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY "Cars"."Vehicle"
    ADD CONSTRAINT "Vehicle_pkey" PRIMARY KEY (vin);
 B   ALTER TABLE ONLY "Cars"."Vehicle" DROP CONSTRAINT "Vehicle_pkey";
       Cars            postgres    false    223            �           2606    16568    Vehicle_type Vehicle_type_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY "Cars"."Vehicle_type"
    ADD CONSTRAINT "Vehicle_type_pkey" PRIMARY KEY (type);
 L   ALTER TABLE ONLY "Cars"."Vehicle_type" DROP CONSTRAINT "Vehicle_type_pkey";
       Cars            postgres    false    222            �           2606    16575    Vehicle ak_vehicle 
   CONSTRAINT     s   ALTER TABLE ONLY "Cars"."Vehicle"
    ADD CONSTRAINT ak_vehicle UNIQUE (model, number_plate, year_of_manufacture);
 >   ALTER TABLE ONLY "Cars"."Vehicle" DROP CONSTRAINT ak_vehicle;
       Cars            postgres    false    223    223    223            �           2606    16604    Passenger Passenger_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY "Clients"."Passenger"
    ADD CONSTRAINT "Passenger_pkey" PRIMARY KEY (pass_id);
 I   ALTER TABLE ONLY "Clients"."Passenger" DROP CONSTRAINT "Passenger_pkey";
       Clients            postgres    false    225            �           2606    16640    Ticket Ticket_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY "Clients"."Ticket"
    ADD CONSTRAINT "Ticket_pkey" PRIMARY KEY (ticked_id);
 C   ALTER TABLE ONLY "Clients"."Ticket" DROP CONSTRAINT "Ticket_pkey";
       Clients            postgres    false    229            �           2606    16642    Ticket ak_cl_ticket 
   CONSTRAINT     c   ALTER TABLE ONLY "Clients"."Ticket"
    ADD CONSTRAINT ak_cl_ticket UNIQUE (schedule_id, pass_id);
 B   ALTER TABLE ONLY "Clients"."Ticket" DROP CONSTRAINT ak_cl_ticket;
       Clients            postgres    false    229    229            �           2606    16654    Ticket ak_cl_ticket2 
   CONSTRAINT     i   ALTER TABLE ONLY "Clients"."Ticket"
    ADD CONSTRAINT ak_cl_ticket2 UNIQUE (schedule_id, place_number);
 C   ALTER TABLE ONLY "Clients"."Ticket" DROP CONSTRAINT ak_cl_ticket2;
       Clients            postgres    false    229    229            �           2606    16606    Passenger ak_pass 
   CONSTRAINT     t   ALTER TABLE ONLY "Clients"."Passenger"
    ADD CONSTRAINT ak_pass UNIQUE (lastname, firstname, passport, birthday);
 @   ALTER TABLE ONLY "Clients"."Passenger" DROP CONSTRAINT ak_pass;
       Clients            postgres    false    225    225    225    225            �           2606    16558    Driver Driver_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY "Operations"."Driver"
    ADD CONSTRAINT "Driver_pkey" PRIMARY KEY (driver_id);
 F   ALTER TABLE ONLY "Operations"."Driver" DROP CONSTRAINT "Driver_pkey";
    
   Operations            postgres    false    221            �           2606    16544    Route Route_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY "Operations"."Route"
    ADD CONSTRAINT "Route_pkey" PRIMARY KEY (route_id);
 D   ALTER TABLE ONLY "Operations"."Route" DROP CONSTRAINT "Route_pkey";
    
   Operations            postgres    false    219            �           2606    16614    Schedule Schedule_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY "Operations"."Schedule"
    ADD CONSTRAINT "Schedule_pkey" PRIMARY KEY (schedule_id);
 J   ALTER TABLE ONLY "Operations"."Schedule" DROP CONSTRAINT "Schedule_pkey";
    
   Operations            postgres    false    227            �           2606    16560    Driver ak_driver 
   CONSTRAINT     v   ALTER TABLE ONLY "Operations"."Driver"
    ADD CONSTRAINT ak_driver UNIQUE (lastname, firstname, passport, birthday);
 B   ALTER TABLE ONLY "Operations"."Driver" DROP CONSTRAINT ak_driver;
    
   Operations            postgres    false    221    221    221    221            �           2606    16616    Schedule ak_op_schedule 
   CONSTRAINT     s   ALTER TABLE ONLY "Operations"."Schedule"
    ADD CONSTRAINT ak_op_schedule UNIQUE (vin, date_depart, time_depart);
 I   ALTER TABLE ONLY "Operations"."Schedule" DROP CONSTRAINT ak_op_schedule;
    
   Operations            postgres    false    227    227    227            �           2606    16546    Route ak_route 
   CONSTRAINT     e   ALTER TABLE ONLY "Operations"."Route"
    ADD CONSTRAINT ak_route UNIQUE (depart, arrive, distance);
 @   ALTER TABLE ONLY "Operations"."Route" DROP CONSTRAINT ak_route;
    
   Operations            postgres    false    219    219    219            �           2606    16581    Vehicle fk_type_vehicle    FK CONSTRAINT     �   ALTER TABLE ONLY "Cars"."Vehicle"
    ADD CONSTRAINT fk_type_vehicle FOREIGN KEY (type) REFERENCES "Cars"."Vehicle_type"(type) ON UPDATE CASCADE ON DELETE SET DEFAULT;
 C   ALTER TABLE ONLY "Cars"."Vehicle" DROP CONSTRAINT fk_type_vehicle;
       Cars          postgres    false    222    4767    223            �           2606    16648    Ticket fk_pass    FK CONSTRAINT     �   ALTER TABLE ONLY "Clients"."Ticket"
    ADD CONSTRAINT fk_pass FOREIGN KEY (pass_id) REFERENCES "Clients"."Passenger"(pass_id) ON UPDATE CASCADE;
 =   ALTER TABLE ONLY "Clients"."Ticket" DROP CONSTRAINT fk_pass;
       Clients          postgres    false    225    4773    229            �           2606    16643    Ticket fk_schedule    FK CONSTRAINT     �   ALTER TABLE ONLY "Clients"."Ticket"
    ADD CONSTRAINT fk_schedule FOREIGN KEY (schedule_id) REFERENCES "Operations"."Schedule"(schedule_id) ON UPDATE CASCADE;
 A   ALTER TABLE ONLY "Clients"."Ticket" DROP CONSTRAINT fk_schedule;
       Clients          postgres    false    229    4777    227            �           2606    16627    Schedule fk_driver    FK CONSTRAINT     �   ALTER TABLE ONLY "Operations"."Schedule"
    ADD CONSTRAINT fk_driver FOREIGN KEY (driver_id) REFERENCES "Operations"."Driver"(driver_id) ON UPDATE CASCADE ON DELETE SET NULL;
 D   ALTER TABLE ONLY "Operations"."Schedule" DROP CONSTRAINT fk_driver;
    
   Operations          postgres    false    221    4763    227            �           2606    16617    Schedule fk_route    FK CONSTRAINT     �   ALTER TABLE ONLY "Operations"."Schedule"
    ADD CONSTRAINT fk_route FOREIGN KEY (route_id) REFERENCES "Operations"."Route"(route_id) ON UPDATE CASCADE;
 C   ALTER TABLE ONLY "Operations"."Schedule" DROP CONSTRAINT fk_route;
    
   Operations          postgres    false    219    227    4759            �           2606    16622    Schedule fk_vehicle    FK CONSTRAINT     �   ALTER TABLE ONLY "Operations"."Schedule"
    ADD CONSTRAINT fk_vehicle FOREIGN KEY (vin) REFERENCES "Cars"."Vehicle"(vin) ON UPDATE CASCADE;
 E   ALTER TABLE ONLY "Operations"."Schedule" DROP CONSTRAINT fk_vehicle;
    
   Operations          postgres    false    227    223    4769            N   �   x�m��
�`���)�J�kz�}nusq�R�
�.n�"� ���]�D��E]r9�����j�n�R�l���ф�h��� 8�Y�tBPh!�
x�g=�;��B�L>�x�k��~�Z<��`yP"�o���z �x���"�"~PI�q��QVB�ˮ�'�����i/�ƙ�/����w�Qf��@�2� ݢa�]�      M   q   x���/Q(N-�47�0����/캰��& ީp��b���о{9-�
&\�t�	��oT����za˅�v\�	6U��=6\�}�(i�)���}��b�.��1z\\\ e-T�      P   �  x�m�;Nk1�k{ހь�g4�HW�@
EB�xQ@�} n�(�(�����aΎ�q	WI|����~�����g��oG�����`�Y��R۝�sLs����qw�b4)��s)E9@��,x��n�ਧ�{%bNp�U�������;�1t���M-Mi��1M���3����d��$6�["�bĄ�h��Z �֝��d��]}��7!��rS����ltT���C����/�q�d3&D��c�����$~F�ʋ�ēw�{�8q��R���	h�ӑ���.�\�N�Kv���q/r<jh��d�br�346��j=��'�2\�,Ӛ2��g��:� ��&�E�X/M�,�{Ƶ��\Z�R�+�X�W8",�0G�5Xt�H�� �l%�i���lJ&�I��s��d��zoKk�Zrn.      T   P   x�U���0�3
0,�p�"�,N&����%O��Pncޙ�I���7_&hiZ���(�0��H�u=1*2F�W\���      L   �   x�u�1�0Eg�>@��nڕ�+'�a3[�P���NH���퟼���^��/��!�M[K���s�TB�@��3,+�4]��P`o��
��j�I��a����S
��>�#���&�������D�`�|�\�zч�����t�}V&��Lb�&$�$,=qV�1�O+%ܸqν3bk�      J   ~   x�3�0�¾��v]�ta�I@NÅ}�^�za���1�����g	�)�$�F�J�J343�\lj�saÅ� ANCSCcNC���JC#+S�s4-�/li���ihhjUllelʙ����� yY      R   V   x�mʻ�0��y��8Χ�e�9О�CQ�yi��)s=��� <H�X�\�aH߻��p��ޱ+鷯�o�0G�HD�B�     
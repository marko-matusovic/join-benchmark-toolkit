CREATE TABLE table_a_sm (
    id integer NOT NULL PRIMARY KEY,
    val character varying(64),
    ref integer NOT NULL,
);

CREATE TABLE table_b_sm (
    id integer NOT NULL PRIMARY KEY,
    val character varying(64),
    ref integer NOT NULL,
);

CREATE TABLE table_a_md (
    id integer NOT NULL PRIMARY KEY,
    val character varying(64),
    ref integer NOT NULL,
);

CREATE TABLE table_b_md (
    id integer NOT NULL PRIMARY KEY,
    val character varying(64),
    ref integer NOT NULL,
);

CREATE TABLE table_a_lg (
    id integer NOT NULL PRIMARY KEY,
    val character varying(64),
    ref integer NOT NULL,
);

CREATE TABLE table_b_lg (
    id integer NOT NULL PRIMARY KEY,
    val character varying(64),
    ref integer NOT NULL,
);
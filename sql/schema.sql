--
-- User accounts table. Every user, regardless of whether they
-- have a pita, should have an account.
--
CREATE TABLE IF NOT EXISTS accounts (
    aid         serial primary key,
    uuid        text not null,
    name        varchar(40) default null,
    phone       bigint default null,
    email       varchar(100) default null,
    key         text,
    created     timestamp default now(),
    last_seen   timestamp default now(),
    latitude    float,
    longitude   float,
    loc         geometry(POINT,4326),
    loc_time    timestamp default null
);

CREATE INDEX idx_accounts_loc ON accounts USING GIST(loc);

--
-- User locations
--
CREATE TABLE IF NOT EXISTS locations (
    lid         serial primary key,
    aid         integer references accounts(aid),
    time        timestamp default now(),
    latitude    float,
    longitude   float,
    loc         geometry(POINT,4326)
);

--
-- Table for logging errors, both on the server and on the client.
--
CREATE TYPE error_type AS ENUM('server', 'client', 'bad_request', 'user', 'access_denied');

CREATE TABLE IF NOT EXISTS errors (
    eid         serial primary key,
    type        error_type not null,
    aid         integer references accounts(aid),
    time        timestamp default now(),
    ip          text,
    message     text not null default ''
);

--
-- Stores all existing Pitas.
--
CREATE TYPE pita_state AS ENUM('egg', 'alive', 'dead', 'disowned', 'on the lamb');

CREATE TABLE IF NOT EXISTS pitas (
    pid         serial primary key,
    aid         integer not null references accounts(aid),
    state       pita_state not null default 'egg',
    parent_a    integer references pitas(pid),
    parent_b    integer references pitas(pid),
    name        text,
    body_hue    float not null,
    spots_hue   float not null,
    tail_hue    float not null,
    has_spots   boolean default false,
    happiness   float not null default 100,
    hunger      float not null default 100,
    sleepiness  float not null default 100
);

--
-- Stores informations about events within a Pita's
-- lifetime.
--
CREATE TYPE pita_event_type AS ENUM('conception', 'born', 'died', 'disowned', 'ran away');

CREATE TABLE IF NOT EXISTS pita_events (
    peid            serial primary key,
    pid             integer not null references pitas(pid),
    aid             integer not null references accounts(aid),
    event_type      pita_event_type,
    time            timestamp default now()
);

--
-- Stores information about photos submitted from clients.
--
CREATE TABLE IF NOT EXISTS logged_photos (
    pid             serial primary key,
    aid             integer not null references accounts(aid),
    time            timestamp default now(),
    ext             text not null,
    saved           boolean default false,
    context         text
);

--
-- Stores dictionary words for generating pita names.
--
CREATE TYPE word_part_of_speech AS ENUM('noun', 'adjective');

CREATE TABLE IF NOT EXISTS dictionary_words (
    wid             serial primary key,
    word            text not null,
    pos             word_part_of_speech
);

--
-- User accounts table. Every user, regardless of whether they
-- have a pita, should have an account.
--
CREATE TABLE IF NOT EXISTS accounts (
    aid         serial primary key,
    name        varchar(40) not null, 
    phone       bigint,
    email       varchar(100),
    key         text,
    created     timestamp default now(),
    last_seen   timestamp default now(),
    loc         Point default null,
    loc_time    timestamp default null
);

--
-- Table for logging errors, both on the server and on the client.
--
CREATE TYPE error_type AS ENUM('server', 'client', 'bad_request', 'user');

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
    parent_b    integer references pitas(pid)
);

--
-- Stores informations about events within a Pita's
-- lifetime.
--
CREATE TYPE pita_event_type AS ENUM('born', 'died', 'disowned', 'ran away');

CREATE TABLE IF NOT EXISTS pita_events (
    peid            serial primary key,
    pid             integer not null references pitas(pid),
    aid             integer not null references accounts(aid),
    time            timestamp default now()
);

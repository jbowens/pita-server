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

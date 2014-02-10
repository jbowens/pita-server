--
-- User accounts table. Every user, regardless of whether they
-- have a pita, should have an account.
--
CREATE TABLE IF NOT EXISTS accounts (
    aid         serial primary key,
    name        varchar(40) not null, 
    phone       integer,
    email       varchar(100)
);

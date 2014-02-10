--
-- Stores all existing Pitas.
--
CREATE TABLE IF NOT EXISTS pitas (
    pid         serial,
    aid         integer not null references accounts(aid),
    born        boolean not null default false
);

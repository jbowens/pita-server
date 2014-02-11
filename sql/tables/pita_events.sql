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

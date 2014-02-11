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

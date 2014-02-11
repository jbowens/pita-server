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

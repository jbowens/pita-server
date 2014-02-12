--
-- Drops all the tables.
--
DROP TABLE IF EXISTS logged_photos CASCADE;
DROP TABLE IF EXISTS pita_events CASCADE;
DROP TABLE IF EXISTS errors CASCADE;
DROP TABLE IF EXISTS locations CASCADE;
DROP TABLE IF EXISTS pitas CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;

--
-- Drop any custom types too.
--
DROP TYPE IF EXISTS error_type CASCADE;
DROP TYPE IF EXISTS pita_state CASCADE;
DROP TYPE IF EXISTS pita_event_type CASCADE;

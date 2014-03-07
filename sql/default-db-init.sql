--
-- Creates the default development db instance. This
-- creates the database, database user, and assigns
-- appropriate privileges. This should be run as a
-- postgresql superuser.
--
CREATE ROLE pita LOGIN;
CREATE DATABASE mylittlepita OWNER pita;
GRANT ALL PRIVILEGES ON DATABASE mylittlepita TO pita;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO pita;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO pita;

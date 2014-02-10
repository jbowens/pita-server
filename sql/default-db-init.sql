--
-- Creates the default development db instance. This
-- creates the database, database user, and assigns
-- appropriate privileges. This should be run as a
-- postgresql superuser.
--
CREATE ROLE pita LOGIN;
CREATE DATABASE mylittlepita OWNER pita;

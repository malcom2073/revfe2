-- Revert revfe2:appschema from pg

BEGIN;

-- XXX Add DDLs here.
-- Drops absolutely everything, since this is the very first one.
DROP SCHEMA public CASCADE;


COMMIT;

-- Deploy revfe2:appschema to pg

BEGIN;

-- XXX Add DDLs here.
CREATE SCHEMA public AUTHORIZATION postgres;

COMMIT;

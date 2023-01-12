-- Verify revfe2:appschema on pg

BEGIN;

-- XXX Add verifications here.

SELECT pg_catalog.has_schema_privilege('public', 'usage');

ROLLBACK;

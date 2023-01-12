-- Verify revfe2:usergroups on pg

BEGIN;

-- XXX Add verifications here.

SELECT id, name, username, email, password, validated, siteadmin
  FROM public.users
WHERE FALSE;

SELECT id, name
  FROM public.groups
WHERE FALSE;

SELECT id, name, description
  FROM public.permissions
WHERE FALSE;

SELECT id, permission_id, group_id
  FROM public.grouppermissions
WHERE FALSE;

ROLLBACK;

-- Revert revfe2:usergroups from pg

BEGIN;

-- XXX Add DDLs here.

DROP TABLE public.usergroups;

DROP TABLE public.grouppermissions;

DROP TABLE public.permissions;

DROP TABLE public.users;

DROP TABLE public.groups;

COMMIT;

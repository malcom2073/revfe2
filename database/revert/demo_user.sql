-- Revert revfe2:demo_user from pg

BEGIN;

-- XXX Add DDLs here.
 -- Delete the demo user and groups
    DELETE FROM public.usergroups WHERE user_id = (SELECT id FROM public.users WHERE email='malcom@mike.com') and group_id = (SELECT id FROM public.groups WHERE name='Admin');
    DELETE FROM public.usergroups WHERE user_id = (SELECT id FROM public.users WHERE email='abby@mike.com') and group_id = (SELECT id FROM public.groups WHERE name='Members');

    DELETE FROM public.groups where name = 'Admin';
    DELETE FROM public.groups where name = 'Members';
    DELETE FROM public.groups where name = 'Newbie';
    DELETE FROM public.users where email = 'malcom@mike.com';
    DELETE FROM public.users where email = 'abby@mike.com';
    

COMMIT;

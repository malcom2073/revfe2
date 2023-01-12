-- Deploy revfe2:demo_user to pg
-- requires: usergroups

BEGIN;

-- XXX Add DDLs here.
--    admingroup = Group(name="Admin",permissions=[userlistperm])
--    regular = Group(name="Members",permissions=[userlistperm])
--    initial = Group(name="Newbie",permissions=[])
--    user = User(name="Mike",username="malcom2073",password="12345",email="malcom@mike.com",groups=[admingroup],validated=True,siteadmin=True)
--    user = User(name="Abigail",username="butterfly2003",password="12345",email="abby@mike.com",groups=[admingroup],validated=True)

    INSERT INTO public.groups (name) VALUES('Admin');

    INSERT INTO public.groups (name) VALUES('Members');
    INSERT INTO public.groups (name) VALUES('Newbie');

    INSERT INTO public.users(name,username,email,password,validated,siteadmin) VALUES('Mike','malcom2073','malcom@mike.com','12345','true','true');
    INSERT INTO public.users(name,username,email,password,validated,siteadmin) VALUES('Abigail','butterfly2003','abby@mike.com','54321','false','false');


    INSERT INTO public.usergroups(user_id,group_id) VALUES ((SELECT id FROM public.users WHERE email='malcom@mike.com'),(SELECT id FROM public.groups WHERE name='Admin'));
    INSERT INTO public.usergroups(user_id,group_id) VALUES ((SELECT id FROM public.users WHERE email='abby@mike.com'),(SELECT id FROM public.groups WHERE name='Members'));
COMMIT;

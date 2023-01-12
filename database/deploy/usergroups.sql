-- Deploy revfe2:usergroups to pg
-- requires: appschema

BEGIN;

CREATE TABLE public.users (
	id serial4 NOT NULL,
	name varchar(256) NULL,
	username varchar(256) NULL,
	email varchar(256) NULL,
	password varchar(256) NULL,
	validated bool NOT NULL,
	siteadmin bool NOT NULL,
	CONSTRAINT "_email_uc" UNIQUE (email),
	CONSTRAINT users_pkey PRIMARY KEY (id)
);

CREATE TABLE public.groups (
	id serial4 NOT NULL,
	name varchar(256) NULL,
	CONSTRAINT "_group_name_uc" UNIQUE (name),
	CONSTRAINT groups_pkey PRIMARY KEY (id)
);

CREATE TABLE public.usergroups (
	id serial4 NOT NULL,
	user_id int4 NULL,
	group_id int4 NULL,
	CONSTRAINT usergroups_pkey PRIMARY KEY (id)
);

ALTER TABLE public.usergroups ADD CONSTRAINT usergroups_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id);
ALTER TABLE public.usergroups ADD CONSTRAINT usergroups_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);

CREATE TABLE public.permissions (
	id serial4 NOT NULL,
	name varchar(256) NULL,
	description varchar(256) NULL,
	CONSTRAINT "_permissions_name_uc" UNIQUE (name),
	CONSTRAINT permissions_pkey PRIMARY KEY (id)
);

CREATE TABLE public.grouppermissions (
	id serial4 NOT NULL,
	permission_id int4 NULL,
	group_id int4 NULL,
	CONSTRAINT grouppermissions_pkey PRIMARY KEY (id)
);

ALTER TABLE public.grouppermissions ADD CONSTRAINT grouppermissions_group_id_fkey FOREIGN KEY (group_id) REFERENCES public."groups"(id);
ALTER TABLE public.grouppermissions ADD CONSTRAINT grouppermissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id);

COMMIT;
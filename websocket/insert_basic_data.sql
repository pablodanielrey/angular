

insert into profile.users (id,dni,name,lastname) values ('1','1','admin','admin');
insert into credentials.user_password (id,user_id,username,password) values ('1','1','admin','admin');
insert into credentials.auth_profile (user_id,profile) values ('1','ADMIN');

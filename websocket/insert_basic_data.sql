

insert into profile.users (id,dni,name,lastname) values ('1','1','admin','admin');
insert into credentials.user_password (id,user_id,username,password) values ('1','1','admin','admin');
insert into credentials.auth_profile (user_id,profile) values ('1','ADMIN');
insert into credentials.auth_profile (user_id,profile) values ('1','ADMIN-TUTOR');
insert into credentials.auth_profile (user_id,profile) values ('1','ADMIN-ASSISTANCE');


insert into assistance.justifications (id,name) values ('e0dfcef6-98bb-4624-ae6c-960657a9a741','Ausente con aviso')
insert into assistance.justifications (id,name) values ('48773fd7-8502-4079-8ad5-963618abe725','Compensatorio')
insert into assistance.justifications (id,name) values ('fa64fdbd-31b0-42ab-af83-818b3cbecf46','Boleta de Salida')
insert into assistance.justifications (id,name) values ('4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb','Art 102')
insert into assistance.justifications (id,name) values ('b70013e3-389a-46d4-8b98-8e4ab75335d0','Pre-Exámen')
insert into assistance.justifications (id,name) values ('76bc064a-e8bf-4aa3-9f51-a3c4483a729a','Licencia Anual Ordinaria')
insert into assistance.justifications (id,name) values ('50998530-10dd-4d68-8b4a-a4b7a87f3972','Resolución')



insert into profile.users (id,dni,name,lastname) values ('1','1','admin','admin');
insert into credentials.user_password (id,user_id,username,password) values ('1','1','admin','admin');
insert into credentials.auth_profile (user_id,profile) values ('1','ADMIN');
insert into credentials.auth_profile (user_id,profile) values ('1','ADMIN-TUTOR');
insert into credentials.auth_profile (user_id,profile) values ('1','ADMIN-ASSISTANCE');





/*
  justificaciones de la facultad de económicas
*/
insert into assistance.justifications (id,name) values ('e0dfcef6-98bb-4624-ae6c-960657a9a741','Ausente con aviso');
insert into assistance.justifications (id,name) values ('48773fd7-8502-4079-8ad5-963618abe725','Compensatorio');
insert into assistance.justifications (id,name) values ('fa64fdbd-31b0-42ab-af83-818b3cbecf46','Boleta de Salida');
insert into assistance.justifications (id,name) values ('4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb','Art 102');
insert into assistance.justifications (id,name) values ('b70013e3-389a-46d4-8b98-8e4ab75335d0','Pre-Exámen');
insert into assistance.justifications (id,name) values ('76bc064a-e8bf-4aa3-9f51-a3c4483a729a','Licencia Anual Ordinaria');
insert into assistance.justifications (id,name) values ('50998530-10dd-4d68-8b4a-a4b7a87f3972','Resolución 638');
insert into assistance.justifications (id,name) values ('f9baed8a-a803-4d7f-943e-35c436d5db46','Licencia Médica Corta Duración');
insert into assistance.justifications (id,name) values ('a93d3af3-4079-4e93-a891-91d5d3145155','Licencia Médica Largo Tratamiento');
insert into assistance.justifications (id,name) values ('b80c8c0e-5311-4ad1-94a7-8d294888d770','Licencia Médica Atención Familiar');
insert into assistance.justifications (id,name) values ('478a2e35-51b8-427a-986e-591a9ee449d8','Justificado por Médico');
insert into assistance.justifications (id,name) values ('5ec903fb-ddaf-4b6c-a2e8-929c77d8256f','Feriado');
insert into assistance.justifications (id,name) values ('874099dc-42a2-4941-a2e1-17398ba046fc','Paro');
insert into assistance.justifications (id,name) values ('b309ea53-217d-4d63-add5-80c47eb76820','Cumpleaños');
insert into assistance.justifications (id,name) values ('0cd276aa-6d6b-4752-abe5-9258dbfd6f09','Duelo');
insert into assistance.justifications (id,name) values ('e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b','Donación de Sangre');
insert into assistance.justifications (id,name) values ('cb2b4583-2f44-4db0-808c-4e36ee059efe','Boleta en Comisión');
insert into assistance.justifications (id,name) values ('70e0951f-d378-44fb-9c43-f402cbfc63c8','Art');
insert into assistance.justifications (id,name) values ('3d486aa0-745a-4914-a46d-bc559853d367','Inbumbencias Climáticas');


/*FALTA BOLETA EN COMISION*/



/*
  2 formas de generar el rol de autorizar en las oficinas raiz
*/
insert into assistance.offices_roles (user_id,role,office_id) select '1','autoriza',id from assistance.offices o where o.parent is null;
insert into assistance.offices_roles (user_id,role,office_id) select p.id,'autoriza',o.id from assistance.offices o, profile.users p where o.parent is null and p.dni in ('1');

/*
  2 formas distintas de generar autorizaciones para las horas extras que son pedidas por las personas
*/
insert into assistance.offices_roles (user_id,role,office_id) select '1','horas-extras',id from assistance.offices o where o.parent is null;
insert into assistance.offices_roles (user_id,role,office_id) select p.id,'horas-extras',o.id from assistance.offices o, profile.users p where o.parent is null and p.dni in ('1');


/*
  2 formas distintas de generar el rol de realizar justificaciones especiales en las oficinas raiz
*/
insert into assistance.offices_roles (user_id,role,office_id) select '1','realizar-solicitud',id from assistance.offices o where o.parent is null;
insert into assistance.offices_roles (user_id,role,office_id) select p.id,'realizar-solicitud',o.id from assistance.offices o, profile.users p where o.parent is null and p.dni in ('1');

/*
  2 formas distintas de generar el rol de realizar justificaciones especiales por una autoridad en las oficinas raiz
*/
insert into assistance.offices_roles (user_id,role,office_id) select '1','realizar-solicitud-admin',id from assistance.offices o where o.parent is null;
insert into assistance.offices_roles (user_id,role,office_id) select p.id,'realizar-solicitud-admin',o.id from assistance.offices o, profile.users p where o.parent is null and p.dni in ('1');

/*
  perfil de Administrador de asistencia. por ahora no es muy distinto.
*/
insert into credentials.auth_profile (user_id,profile) select id,'ADMIN-ASSISTANCE' from profile.users where dni in ('27294557','31381082','30001823','29694757');






/*
  /////////////////////////// ECONO ASISTENCIA ///////////////////
  datos especificos de econo.
*/

/*
  autorizadores de todo y de horas extras.
  24892148 - pablo díaz barcala
  31993212 - adrián lavigna
  30057880 - carlos villalba

  27528150 - Julio Ciappa
  32393755 - Pablo Lozada

*/
delete from assistance.offices_roles where user_id in (select id from profile.users where dni in ('1','24892148','31993212','30057880','27528150','32393755'));
insert into assistance.offices_roles (user_id,role,office_id,send_mail) select p.id,'autoriza',o.id,false from assistance.offices o, profile.users p where o.parent is null and p.dni in ('1','24892148','31993212','30057880');
insert into assistance.offices_roles (user_id,role,office_id,send_mail) select p.id,'autoriza',o.id,true from assistance.offices o, profile.users p where o.parent is null and p.dni in ('27528150','32393755');

insert into assistance.offices_roles (user_id,role,office_id,send_mail) select p.id,'horas-extras',o.id,true from assistance.offices o, profile.users p where o.parent is null and p.dni in ('1','24892148','31993212','30057880','27528150','32393755');

insert into assistance.offices_roles (user_id,role,office_id) select p.id,'realizar-solicitud',o.id from assistance.offices o, profile.users p where o.parent is null and p.dni in ('1','24892148','31993212','30057880','27528150','32393755');


/*
creo los checks de precencia para todos los usuarios, menos los jefes que no se deben chequear. y los cargos docentes que están
solo para autorizar dentro del sistema.
*/
insert into assistance.checks (id,user_id,type,date,enable) select id,id,'PRESENCE','2015-04-01 00:00:00',true from profile.users as u where u.id in (select user_id from credentials.auth_profile as ap where ap.profile like 'USER-ASSISTANCE');
delete from assistance.checks where user_id in (select id from profile.users where dni in ('1','24892148','31993212','30057880'));
delete from assistance.checks where user_id in (select id from profile.users where dni in ('27294557'));
/*
  jefes docentes
*/
delete from assistance.checks where user_id in (select id from profile.users where dni in ('24771757','8700794','25952190'));

/*
  para agregar de prueba nuestros dnis al perfil admin-assistance
*/
insert into credentials.auth_profile (user_id,profile) select id,'ADMIN-ASSISTANCE' from profile.users where dni in ('27294557','31381082','30001823','29694757');







/*
  /////////////////////////////////////////////////////////////
  //////////// Sistema de inserción laboral
  /////////////////////////////////////////////////
*/


insert into credentials.auth_profile (user_id,profile) select id,'ADMIN-LABORALINSERTION' from profile.users where dni in ('27294557','31381082','30001823','29694757');

/*
  usuario de paula y de lucas
*/
insert into credentials.auth_profile (user_id,profile) select id,'ADMIN-LABORALINSERTION' from profile.users where dni in ('29763750','32066197');

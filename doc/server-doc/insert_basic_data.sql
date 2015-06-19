

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
insert into assistance.justifications (id,name) values ('3d486aa0-745a-4914-a46d-bc559853d367','Incumbencias Climáticas');
insert into assistance.justifications (id,name) values ('5c548eab-b8fc-40be-bb85-ef53d594dca9','Día del Bibliotecario');
insert into assistance.justifications (id,name) values ('508a9b3a-e326-4b77-a103-3399cb65f82a','Asistencia a Congresos/Capacitación - art 97 dec 366');


insert into assistance.justifications (id,name) values ('7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7','Entrada Tarde Justificada');
insert into assistance.justifications (id,name) values ('c32eb2eb-882b-4905-8e8f-c03405cee727','Justificado Por Autoridad');
insert into assistance.justifications (id,name) values ('aa41a39e-c20e-4cc4-942c-febe95569499','Licencia Médica Pre-Natal. Art 106P');
insert into assistance.justifications (id,name) values ('f7464e86-8b9e-4415-b370-b44b624951ca','Receso de Invierno');
insert into assistance.justifications (id,name) values ('e249bfce-5af3-4d99-8509-9adc2330700b','Nacimiento');
insert into assistance.justifications (id,name) values ('5289eac5-9221-4a09-932c-9f1e3d099a47','Concurso');
insert into assistance.justifications (id,name) values ('68bf4c98-984d-4b71-98b0-4165c69d62ce','Licencia Médica Por Maternidad');
insert into assistance.justifications (id,name) values ('30a249d5-f90c-4666-aec6-34c53b62a447','Matrimonio');
insert into assistance.justifications (id,name) values ('1c14a13c-2358-424f-89d3-d639a9404579','Licencia Sin Goce De Sueldo');
insert into assistance.justifications (id,name) values ('3fb52f24-3eff-4ca2-8133-c7a3abfc7262','Justificado Horario');
insert into assistance.justifications (id,name) values ('bfaebb07-8d08-4551-b264-85eb4cab6ef1','Suspención');
insert into assistance.justifications (id,name) values ('7747e3ff-bbe2-4f2e-88f7-9cc624a242a9','Viaje');





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
  prefiles para el sistema de oficinas
*/
insert into credentials.auth_profile (user_id,profile) select id,'ADMIN-OFFICES' from profile.users where dni in ('1');


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



/*
 *"justifications" asociadas a las "position"
 */
/* a2 */
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'e0dfcef6-98bb-4624-ae6c-960657a9a741');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '48773fd7-8502-4079-8ad5-963618abe725');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'b70013e3-389a-46d4-8b98-8e4ab75335d0');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '50998530-10dd-4d68-8b4a-a4b7a87f3972');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'b309ea53-217d-4d63-add5-80c47eb76820');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'cb2b4583-2f44-4db0-808c-4e36ee059efe');

/* a3 */
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'e0dfcef6-98bb-4624-ae6c-960657a9a741');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '48773fd7-8502-4079-8ad5-963618abe725');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'b70013e3-389a-46d4-8b98-8e4ab75335d0');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '50998530-10dd-4d68-8b4a-a4b7a87f3972');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'b309ea53-217d-4d63-add5-80c47eb76820');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'cb2b4583-2f44-4db0-808c-4e36ee059efe');

/* a4 */
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'e0dfcef6-98bb-4624-ae6c-960657a9a741');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '48773fd7-8502-4079-8ad5-963618abe725');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'b70013e3-389a-46d4-8b98-8e4ab75335d0');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '50998530-10dd-4d68-8b4a-a4b7a87f3972');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'b309ea53-217d-4d63-add5-80c47eb76820');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'cb2b4583-2f44-4db0-808c-4e36ee059efe');

/* a5 */
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'e0dfcef6-98bb-4624-ae6c-960657a9a741');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '48773fd7-8502-4079-8ad5-963618abe725');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'b70013e3-389a-46d4-8b98-8e4ab75335d0');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '50998530-10dd-4d68-8b4a-a4b7a87f3972');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'b309ea53-217d-4d63-add5-80c47eb76820');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'cb2b4583-2f44-4db0-808c-4e36ee059efe');

/* a6 */
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'e0dfcef6-98bb-4624-ae6c-960657a9a741');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '48773fd7-8502-4079-8ad5-963618abe725');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'b70013e3-389a-46d4-8b98-8e4ab75335d0');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '50998530-10dd-4d68-8b4a-a4b7a87f3972');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'b309ea53-217d-4d63-add5-80c47eb76820');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'cb2b4583-2f44-4db0-808c-4e36ee059efe');

/* a7 */
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'e0dfcef6-98bb-4624-ae6c-960657a9a741');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '48773fd7-8502-4079-8ad5-963618abe725');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'b70013e3-389a-46d4-8b98-8e4ab75335d0');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '50998530-10dd-4d68-8b4a-a4b7a87f3972');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'b309ea53-217d-4d63-add5-80c47eb76820');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'cb2b4583-2f44-4db0-808c-4e36ee059efe');

/* e2 */
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'e0dfcef6-98bb-4624-ae6c-960657a9a741');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '48773fd7-8502-4079-8ad5-963618abe725');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'b70013e3-389a-46d4-8b98-8e4ab75335d0');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '50998530-10dd-4d68-8b4a-a4b7a87f3972');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'b309ea53-217d-4d63-add5-80c47eb76820');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'cb2b4583-2f44-4db0-808c-4e36ee059efe');

/* e3 */
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'e0dfcef6-98bb-4624-ae6c-960657a9a741');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '48773fd7-8502-4079-8ad5-963618abe725');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'b70013e3-389a-46d4-8b98-8e4ab75335d0');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '50998530-10dd-4d68-8b4a-a4b7a87f3972');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'b309ea53-217d-4d63-add5-80c47eb76820');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'cb2b4583-2f44-4db0-808c-4e36ee059efe');

/* e4 */
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'e0dfcef6-98bb-4624-ae6c-960657a9a741');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '48773fd7-8502-4079-8ad5-963618abe725');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'b70013e3-389a-46d4-8b98-8e4ab75335d0');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '50998530-10dd-4d68-8b4a-a4b7a87f3972');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'b309ea53-217d-4d63-add5-80c47eb76820');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'cb2b4583-2f44-4db0-808c-4e36ee059efe');

/* e5 */
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'e0dfcef6-98bb-4624-ae6c-960657a9a741');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '48773fd7-8502-4079-8ad5-963618abe725');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'b70013e3-389a-46d4-8b98-8e4ab75335d0');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '50998530-10dd-4d68-8b4a-a4b7a87f3972');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'b309ea53-217d-4d63-add5-80c47eb76820');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'cb2b4583-2f44-4db0-808c-4e36ee059efe');

/* e6 */
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'e0dfcef6-98bb-4624-ae6c-960657a9a741');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '48773fd7-8502-4079-8ad5-963618abe725');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'b70013e3-389a-46d4-8b98-8e4ab75335d0');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '50998530-10dd-4d68-8b4a-a4b7a87f3972');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'b309ea53-217d-4d63-add5-80c47eb76820');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'cb2b4583-2f44-4db0-808c-4e36ee059efe');

/* e7 */
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'e0dfcef6-98bb-4624-ae6c-960657a9a741');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '48773fd7-8502-4079-8ad5-963618abe725');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'b70013e3-389a-46d4-8b98-8e4ab75335d0');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '50998530-10dd-4d68-8b4a-a4b7a87f3972');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'b309ea53-217d-4d63-add5-80c47eb76820');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'cb2b4583-2f44-4db0-808c-4e36ee059efe');


/* gestion */
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'e0dfcef6-98bb-4624-ae6c-960657a9a741');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', '48773fd7-8502-4079-8ad5-963618abe725');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'b70013e3-389a-46d4-8b98-8e4ab75335d0');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', '50998530-10dd-4d68-8b4a-a4b7a87f3972');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'b309ea53-217d-4d63-add5-80c47eb76820');


/* obra */
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', 'e0dfcef6-98bb-4624-ae6c-960657a9a741');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', '48773fd7-8502-4079-8ad5-963618abe725');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', 'b70013e3-389a-46d4-8b98-8e4ab75335d0');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', '50998530-10dd-4d68-8b4a-a4b7a87f3972');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', 'b309ea53-217d-4d63-add5-80c47eb76820');


/* Beca */
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', 'e0dfcef6-98bb-4624-ae6c-960657a9a741');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', '48773fd7-8502-4079-8ad5-963618abe725');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', 'b70013e3-389a-46d4-8b98-8e4ab75335d0');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', '50998530-10dd-4d68-8b4a-a4b7a87f3972');
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', 'b309ea53-217d-4d63-add5-80c47eb76820');



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
insert into assistance.justifications (id,name) values ('e249bfce-5af3-4d99-8509-9adc2330700b','Nacimiento');
insert into assistance.justifications (id,name) values ('5289eac5-9221-4a09-932c-9f1e3d099a47','Concurso');
insert into assistance.justifications (id,name) values ('68bf4c98-984d-4b71-98b0-4165c69d62ce','Licencia Médica Por Maternidad');
insert into assistance.justifications (id,name) values ('30a249d5-f90c-4666-aec6-34c53b62a447','Matrimonio');
insert into assistance.justifications (id,name) values ('1c14a13c-2358-424f-89d3-d639a9404579','Licencia Sin Goce De Sueldo');
insert into assistance.justifications (id,name) values ('3fb52f24-3eff-4ca2-8133-c7a3abfc7262','Justificado Horario');
insert into assistance.justifications (id,name) values ('bfaebb07-8d08-4551-b264-85eb4cab6ef1','Suspensión');
insert into assistance.justifications (id,name) values ('7747e3ff-bbe2-4f2e-88f7-9cc624a242a9','Viaje');

insert into assistance.justifications (id,name) values ('f7464e86-8b9e-4415-b370-b44b624951ca','Receso de Invierno');
insert into assistance.justifications (id,name) values ('5ec903fb-ddaf-4b6c-a2e8-929c77d8256f','Feriado');
insert into assistance.justifications (id,name) values ('874099dc-42a2-4941-a2e1-17398ba046fc','Paro');
insert into assistance.justifications (id,name) values ('6300ad65-537e-41f2-b932-e5a758d22381','Receso de Verano');


/*
  oficina donde se asignan los usuarios importados desde los relojes
*/
insert into offices.offices (id,name) values ('45cc065a-7033-4f00-9b19-d7d097129db3','Asistencia Usuarios Nuevos');



/*
  2 formas de generar el rol de autorizar en las oficinas raiz
*/
insert into offices.offices_roles (user_id,role,office_id) select '1','autoriza',id from offices.offices o where o.parent is null;
insert into offices.offices_roles (user_id,role,office_id) select p.id,'autoriza',o.id from offices.offices o, profile.users p where o.parent is null and p.dni in ('1');

/*
  2 formas de generar el rol de admin-office en las oficinas raiz
*/
insert into offices.offices_roles (user_id,role,office_id) select '1','admin-office',id from offices.offices o where o.parent is null;
insert into offices.offices_roles (user_id,role,office_id) select p.id,'admin-office',o.id from offices.offices o, profile.users p where o.parent is null and p.dni in ('1');

/*
  2 formas distintas de generar autorizaciones para las horas extras que son pedidas por las personas
*/
insert into offices.offices_roles (user_id,role,office_id) select '1','horas-extras',id from offices.offices o where o.parent is null;
insert into offices.offices_roles (user_id,role,office_id) select p.id,'horas-extras',o.id from offices.offices o, profile.users p where o.parent is null and p.dni in ('1');


/*
  2 formas distintas de generar el rol de realizar justificaciones especiales en las oficinas raiz
*/
insert into offices.offices_roles (user_id,role,office_id) select '1','realizar-solicitud',id from offices.offices o where o.parent is null;
insert into offices.offices_roles (user_id,role,office_id) select p.id,'realizar-solicitud',o.id from offices.offices o, profile.users p where o.parent is null and p.dni in ('1');

/*
  2 formas distintas de generar el rol de realizar justificaciones especiales por una autoridad en las oficinas raiz
*/
insert into offices.offices_roles (user_id,role,office_id) select '1','realizar-solicitud-admin',id from offices.offices o where o.parent is null;
insert into offices.offices_roles (user_id,role,office_id) select p.id,'realizar-solicitud-admin',o.id from offices.offices o, profile.users p where o.parent is null and p.dni in ('1');


insert into offices.offices_roles (user_id,role,office_id) select '1','manage-positions',id from offices.offices o where o.parent is null;
insert into offices.offices_roles (user_id,role,office_id) select p.id,'manage-positions',o.id from offices.offices o, profile.users p where o.parent is null and p.dni in ('1');


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
delete from offices.offices_roles where user_id in (select id from profile.users where dni in ('1','24892148','31993212','30057880','27528150','32393755'));
insert into offices.offices_roles (user_id,role,office_id,send_mail) select p.id,'autoriza',o.id,false from offices.offices o, profile.users p where o.parent is null and p.dni in ('1','24892148','31993212','30057880');
insert into offices.offices_roles (user_id,role,office_id,send_mail) select p.id,'autoriza',o.id,true from offices.offices o, profile.users p where o.parent is null and p.dni in ('27528150','32393755');

insert into offices.offices_roles (user_id,role,office_id,send_mail) select p.id,'horas-extras',o.id,true from offices.offices o, profile.users p where o.parent is null and p.dni in ('1','24892148','31993212','30057880','27528150','32393755');

insert into offices.offices_roles (user_id,role,office_id) select p.id,'realizar-solicitud',o.id from offices.offices o, profile.users p where o.parent is null and p.dni in ('1','24892148','31993212','30057880','27528150','32393755');


/*
creo los checks de precencia para todos los usuarios, menos los jefes que no se deben chequear. y los cargos docentes que están
solo para autorizar dentro del sistema.
*/
insert into assistance.checks (id,user_id,type,date,enable) select id,id,'PRESENCE','2015-02-01 00:00:00',true from profile.users as u where u.id in (select user_id from credentials.auth_profile as ap where ap.profile like 'USER-ASSISTANCE');
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
insert into credentials.auth_profile (user_id,profile) select id,'SUPER-ADMIN-OFFICES' from profile.users where dni in ('1');

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
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'e0dfcef6-98bb-4624-ae6c-960657a9a741'); --ausente con aviso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '48773fd7-8502-4079-8ad5-963618abe725'); --Compensatorio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'); --Boleta de Salida
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb'); --Art 102
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'b70013e3-389a-46d4-8b98-8e4ab75335d0'); --Pre-Examen
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a'); --Licencia Anual Ordinaria
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '50998530-10dd-4d68-8b4a-a4b7a87f3972'); --Resolucion 638
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'f9baed8a-a803-4d7f-943e-35c436d5db46'); --Licencia medica corta duracion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'a93d3af3-4079-4e93-a891-91d5d3145155'); --Licencia medica largo tratamiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'b80c8c0e-5311-4ad1-94a7-8d294888d770'); --Licencia medica atencion familiar
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'b309ea53-217d-4d63-add5-80c47eb76820'); --cumple
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '0cd276aa-6d6b-4752-abe5-9258dbfd6f09'); --duelo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b'); --Donacion de Sangre
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'cb2b4583-2f44-4db0-808c-4e36ee059efe'); --Boleta en comision
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '70e0951f-d378-44fb-9c43-f402cbfc63c8'); --ART
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '5c548eab-b8fc-40be-bb85-ef53d594dca9'); --Dia bibliotecario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '508a9b3a-e326-4b77-a103-3399cb65f82a'); --Asistencia cursos capacitacion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7'); --Entrada tarde justificada
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'c32eb2eb-882b-4905-8e8f-c03405cee727'); --Justificado Por Autoridad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'aa41a39e-c20e-4cc4-942c-febe95569499'); --Licencia Medica Pre-Natal. Art 106P
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'f7464e86-8b9e-4415-b370-b44b624951ca'); --Receso de Invierno
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'e249bfce-5af3-4d99-8509-9adc2330700b'); --Nacimiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '5289eac5-9221-4a09-932c-9f1e3d099a47'); --Concurso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '68bf4c98-984d-4b71-98b0-4165c69d62ce'); --Licencia medica por maternidad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '30a249d5-f90c-4666-aec6-34c53b62a447'); --Matrimonio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '1c14a13c-2358-424f-89d3-d639a9404579'); --Licencia Sin Goce De Sueldo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '3fb52f24-3eff-4ca2-8133-c7a3abfc7262'); --Justificado Horario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', 'bfaebb07-8d08-4551-b264-85eb4cab6ef1'); --Suspension
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A2', '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9'); --Viaje





INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'e0dfcef6-98bb-4624-ae6c-960657a9a741'); --ausente con aviso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '48773fd7-8502-4079-8ad5-963618abe725'); --Compensatorio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'); --Boleta de Salida
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb'); --Art 102
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'b70013e3-389a-46d4-8b98-8e4ab75335d0'); --Pre-Examen
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a'); --Licencia Anual Ordinaria
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '50998530-10dd-4d68-8b4a-a4b7a87f3972'); --Resolucion 638
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'f9baed8a-a803-4d7f-943e-35c436d5db46'); --Licencia medica corta duracion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'a93d3af3-4079-4e93-a891-91d5d3145155'); --Licencia medica largo tratamiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'b80c8c0e-5311-4ad1-94a7-8d294888d770'); --Licencia medica atencion familiar
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'b309ea53-217d-4d63-add5-80c47eb76820'); --cumple
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '0cd276aa-6d6b-4752-abe5-9258dbfd6f09'); --duelo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b'); --Donacion de Sangre
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'cb2b4583-2f44-4db0-808c-4e36ee059efe'); --Boleta en comision
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '70e0951f-d378-44fb-9c43-f402cbfc63c8'); --ART
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '5c548eab-b8fc-40be-bb85-ef53d594dca9'); --Dia bibliotecario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '508a9b3a-e326-4b77-a103-3399cb65f82a'); --Asistencia cursos capacitacion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7'); --Entrada tarde justificada
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'c32eb2eb-882b-4905-8e8f-c03405cee727'); --Justificado Por Autoridad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'aa41a39e-c20e-4cc4-942c-febe95569499'); --Licencia Medica Pre-Natal. Art 106P
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'f7464e86-8b9e-4415-b370-b44b624951ca'); --Receso de Invierno
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'e249bfce-5af3-4d99-8509-9adc2330700b'); --Nacimiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '5289eac5-9221-4a09-932c-9f1e3d099a47'); --Concurso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '68bf4c98-984d-4b71-98b0-4165c69d62ce'); --Licencia medica por maternidad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '30a249d5-f90c-4666-aec6-34c53b62a447'); --Matrimonio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '1c14a13c-2358-424f-89d3-d639a9404579'); --Licencia Sin Goce De Sueldo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '3fb52f24-3eff-4ca2-8133-c7a3abfc7262'); --Justificado Horario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', 'bfaebb07-8d08-4551-b264-85eb4cab6ef1'); --Suspension
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A3', '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9'); --Viaje



INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'e0dfcef6-98bb-4624-ae6c-960657a9a741'); --ausente con aviso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '48773fd7-8502-4079-8ad5-963618abe725'); --Compensatorio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'); --Boleta de Salida
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb'); --Art 102
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'b70013e3-389a-46d4-8b98-8e4ab75335d0'); --Pre-Examen
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a'); --Licencia Anual Ordinaria
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '50998530-10dd-4d68-8b4a-a4b7a87f3972'); --Resolucion 638
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'f9baed8a-a803-4d7f-943e-35c436d5db46'); --Licencia medica corta duracion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'a93d3af3-4079-4e93-a891-91d5d3145155'); --Licencia medica largo tratamiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'b80c8c0e-5311-4ad1-94a7-8d294888d770'); --Licencia medica atencion familiar
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'b309ea53-217d-4d63-add5-80c47eb76820'); --cumple
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '0cd276aa-6d6b-4752-abe5-9258dbfd6f09'); --duelo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b'); --Donacion de Sangre
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'cb2b4583-2f44-4db0-808c-4e36ee059efe'); --Boleta en comision
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '70e0951f-d378-44fb-9c43-f402cbfc63c8'); --ART
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '5c548eab-b8fc-40be-bb85-ef53d594dca9'); --Dia bibliotecario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '508a9b3a-e326-4b77-a103-3399cb65f82a'); --Asistencia cursos capacitacion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7'); --Entrada tarde justificada
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'c32eb2eb-882b-4905-8e8f-c03405cee727'); --Justificado Por Autoridad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'aa41a39e-c20e-4cc4-942c-febe95569499'); --Licencia Medica Pre-Natal. Art 106P
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'f7464e86-8b9e-4415-b370-b44b624951ca'); --Receso de Invierno
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'e249bfce-5af3-4d99-8509-9adc2330700b'); --Nacimiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '5289eac5-9221-4a09-932c-9f1e3d099a47'); --Concurso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '68bf4c98-984d-4b71-98b0-4165c69d62ce'); --Licencia medica por maternidad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '30a249d5-f90c-4666-aec6-34c53b62a447'); --Matrimonio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '1c14a13c-2358-424f-89d3-d639a9404579'); --Licencia Sin Goce De Sueldo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '3fb52f24-3eff-4ca2-8133-c7a3abfc7262'); --Justificado Horario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', 'bfaebb07-8d08-4551-b264-85eb4cab6ef1'); --Suspension
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A4', '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9'); --Viaje





INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'e0dfcef6-98bb-4624-ae6c-960657a9a741'); --ausente con aviso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '48773fd7-8502-4079-8ad5-963618abe725'); --Compensatorio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'); --Boleta de Salida
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb'); --Art 102
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'b70013e3-389a-46d4-8b98-8e4ab75335d0'); --Pre-Examen
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a'); --Licencia Anual Ordinaria
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '50998530-10dd-4d68-8b4a-a4b7a87f3972'); --Resolucion 638
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'f9baed8a-a803-4d7f-943e-35c436d5db46'); --Licencia medica corta duracion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'a93d3af3-4079-4e93-a891-91d5d3145155'); --Licencia medica largo tratamiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'b80c8c0e-5311-4ad1-94a7-8d294888d770'); --Licencia medica atencion familiar
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'b309ea53-217d-4d63-add5-80c47eb76820'); --cumple
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '0cd276aa-6d6b-4752-abe5-9258dbfd6f09'); --duelo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b'); --Donacion de Sangre
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'cb2b4583-2f44-4db0-808c-4e36ee059efe'); --Boleta en comision
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '70e0951f-d378-44fb-9c43-f402cbfc63c8'); --ART
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '5c548eab-b8fc-40be-bb85-ef53d594dca9'); --Dia bibliotecario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '508a9b3a-e326-4b77-a103-3399cb65f82a'); --Asistencia cursos capacitacion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7'); --Entrada tarde justificada
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'c32eb2eb-882b-4905-8e8f-c03405cee727'); --Justificado Por Autoridad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'aa41a39e-c20e-4cc4-942c-febe95569499'); --Licencia Medica Pre-Natal. Art 106P
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'f7464e86-8b9e-4415-b370-b44b624951ca'); --Receso de Invierno
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'e249bfce-5af3-4d99-8509-9adc2330700b'); --Nacimiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '5289eac5-9221-4a09-932c-9f1e3d099a47'); --Concurso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '68bf4c98-984d-4b71-98b0-4165c69d62ce'); --Licencia medica por maternidad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '30a249d5-f90c-4666-aec6-34c53b62a447'); --Matrimonio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '1c14a13c-2358-424f-89d3-d639a9404579'); --Licencia Sin Goce De Sueldo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '3fb52f24-3eff-4ca2-8133-c7a3abfc7262'); --Justificado Horario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', 'bfaebb07-8d08-4551-b264-85eb4cab6ef1'); --Suspension
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A5', '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9'); --Viaje







INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'e0dfcef6-98bb-4624-ae6c-960657a9a741'); --ausente con aviso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '48773fd7-8502-4079-8ad5-963618abe725'); --Compensatorio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'); --Boleta de Salida
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb'); --Art 102
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'b70013e3-389a-46d4-8b98-8e4ab75335d0'); --Pre-Examen
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a'); --Licencia Anual Ordinaria
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '50998530-10dd-4d68-8b4a-a4b7a87f3972'); --Resolucion 638
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'f9baed8a-a803-4d7f-943e-35c436d5db46'); --Licencia medica corta duracion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'a93d3af3-4079-4e93-a891-91d5d3145155'); --Licencia medica largo tratamiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'b80c8c0e-5311-4ad1-94a7-8d294888d770'); --Licencia medica atencion familiar
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'b309ea53-217d-4d63-add5-80c47eb76820'); --cumple
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '0cd276aa-6d6b-4752-abe5-9258dbfd6f09'); --duelo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b'); --Donacion de Sangre
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'cb2b4583-2f44-4db0-808c-4e36ee059efe'); --Boleta en comision
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '70e0951f-d378-44fb-9c43-f402cbfc63c8'); --ART
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '5c548eab-b8fc-40be-bb85-ef53d594dca9'); --Dia bibliotecario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '508a9b3a-e326-4b77-a103-3399cb65f82a'); --Asistencia cursos capacitacion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7'); --Entrada tarde justificada
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'c32eb2eb-882b-4905-8e8f-c03405cee727'); --Justificado Por Autoridad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'aa41a39e-c20e-4cc4-942c-febe95569499'); --Licencia Medica Pre-Natal. Art 106P
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'f7464e86-8b9e-4415-b370-b44b624951ca'); --Receso de Invierno
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'e249bfce-5af3-4d99-8509-9adc2330700b'); --Nacimiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '5289eac5-9221-4a09-932c-9f1e3d099a47'); --Concurso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '68bf4c98-984d-4b71-98b0-4165c69d62ce'); --Licencia medica por maternidad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '30a249d5-f90c-4666-aec6-34c53b62a447'); --Matrimonio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '1c14a13c-2358-424f-89d3-d639a9404579'); --Licencia Sin Goce De Sueldo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '3fb52f24-3eff-4ca2-8133-c7a3abfc7262'); --Justificado Horario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', 'bfaebb07-8d08-4551-b264-85eb4cab6ef1'); --Suspension
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A6', '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9'); --Viaje



INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'e0dfcef6-98bb-4624-ae6c-960657a9a741'); --ausente con aviso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '48773fd7-8502-4079-8ad5-963618abe725'); --Compensatorio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'); --Boleta de Salida
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb'); --Art 102
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'b70013e3-389a-46d4-8b98-8e4ab75335d0'); --Pre-Examen
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a'); --Licencia Anual Ordinaria
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '50998530-10dd-4d68-8b4a-a4b7a87f3972'); --Resolucion 638
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'f9baed8a-a803-4d7f-943e-35c436d5db46'); --Licencia medica corta duracion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'a93d3af3-4079-4e93-a891-91d5d3145155'); --Licencia medica largo tratamiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'b80c8c0e-5311-4ad1-94a7-8d294888d770'); --Licencia medica atencion familiar
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'b309ea53-217d-4d63-add5-80c47eb76820'); --cumple
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '0cd276aa-6d6b-4752-abe5-9258dbfd6f09'); --duelo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b'); --Donacion de Sangre
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'cb2b4583-2f44-4db0-808c-4e36ee059efe'); --Boleta en comision
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '70e0951f-d378-44fb-9c43-f402cbfc63c8'); --ART
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '5c548eab-b8fc-40be-bb85-ef53d594dca9'); --Dia bibliotecario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '508a9b3a-e326-4b77-a103-3399cb65f82a'); --Asistencia cursos capacitacion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7'); --Entrada tarde justificada
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'c32eb2eb-882b-4905-8e8f-c03405cee727'); --Justificado Por Autoridad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'aa41a39e-c20e-4cc4-942c-febe95569499'); --Licencia Medica Pre-Natal. Art 106P
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'f7464e86-8b9e-4415-b370-b44b624951ca'); --Receso de Invierno
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'e249bfce-5af3-4d99-8509-9adc2330700b'); --Nacimiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '5289eac5-9221-4a09-932c-9f1e3d099a47'); --Concurso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '68bf4c98-984d-4b71-98b0-4165c69d62ce'); --Licencia medica por maternidad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '30a249d5-f90c-4666-aec6-34c53b62a447'); --Matrimonio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '1c14a13c-2358-424f-89d3-d639a9404579'); --Licencia Sin Goce De Sueldo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '3fb52f24-3eff-4ca2-8133-c7a3abfc7262'); --Justificado Horario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', 'bfaebb07-8d08-4551-b264-85eb4cab6ef1'); --Suspension
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('A7', '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9'); --Viaje





INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'e0dfcef6-98bb-4624-ae6c-960657a9a741'); --ausente con aviso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '48773fd7-8502-4079-8ad5-963618abe725'); --Compensatorio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'); --Boleta de Salida
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb'); --Art 102
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'b70013e3-389a-46d4-8b98-8e4ab75335d0'); --Pre-Examen
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a'); --Licencia Anual Ordinaria
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '50998530-10dd-4d68-8b4a-a4b7a87f3972'); --Resolucion 638
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'f9baed8a-a803-4d7f-943e-35c436d5db46'); --Licencia medica corta duracion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'a93d3af3-4079-4e93-a891-91d5d3145155'); --Licencia medica largo tratamiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'b80c8c0e-5311-4ad1-94a7-8d294888d770'); --Licencia medica atencion familiar
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'b309ea53-217d-4d63-add5-80c47eb76820'); --cumple
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '0cd276aa-6d6b-4752-abe5-9258dbfd6f09'); --duelo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b'); --Donacion de Sangre
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'cb2b4583-2f44-4db0-808c-4e36ee059efe'); --Boleta en comision
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '70e0951f-d378-44fb-9c43-f402cbfc63c8'); --ART
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '5c548eab-b8fc-40be-bb85-ef53d594dca9'); --Dia bibliotecario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '508a9b3a-e326-4b77-a103-3399cb65f82a'); --Asistencia cursos capacitacion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7'); --Entrada tarde justificada
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'c32eb2eb-882b-4905-8e8f-c03405cee727'); --Justificado Por Autoridad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'aa41a39e-c20e-4cc4-942c-febe95569499'); --Licencia Medica Pre-Natal. Art 106P
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'f7464e86-8b9e-4415-b370-b44b624951ca'); --Receso de Invierno
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'e249bfce-5af3-4d99-8509-9adc2330700b'); --Nacimiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '5289eac5-9221-4a09-932c-9f1e3d099a47'); --Concurso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '68bf4c98-984d-4b71-98b0-4165c69d62ce'); --Licencia medica por maternidad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '30a249d5-f90c-4666-aec6-34c53b62a447'); --Matrimonio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '1c14a13c-2358-424f-89d3-d639a9404579'); --Licencia Sin Goce De Sueldo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '3fb52f24-3eff-4ca2-8133-c7a3abfc7262'); --Justificado Horario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', 'bfaebb07-8d08-4551-b264-85eb4cab6ef1'); --Suspension
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E2', '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9'); --Viaje





INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'e0dfcef6-98bb-4624-ae6c-960657a9a741'); --ausente con aviso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '48773fd7-8502-4079-8ad5-963618abe725'); --Compensatorio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'); --Boleta de Salida
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb'); --Art 102
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'b70013e3-389a-46d4-8b98-8e4ab75335d0'); --Pre-Examen
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a'); --Licencia Anual Ordinaria
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '50998530-10dd-4d68-8b4a-a4b7a87f3972'); --Resolucion 638
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'f9baed8a-a803-4d7f-943e-35c436d5db46'); --Licencia medica corta duracion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'a93d3af3-4079-4e93-a891-91d5d3145155'); --Licencia medica largo tratamiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'b80c8c0e-5311-4ad1-94a7-8d294888d770'); --Licencia medica atencion familiar
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'b309ea53-217d-4d63-add5-80c47eb76820'); --cumple
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '0cd276aa-6d6b-4752-abe5-9258dbfd6f09'); --duelo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b'); --Donacion de Sangre
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'cb2b4583-2f44-4db0-808c-4e36ee059efe'); --Boleta en comision
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '70e0951f-d378-44fb-9c43-f402cbfc63c8'); --ART
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '5c548eab-b8fc-40be-bb85-ef53d594dca9'); --Dia bibliotecario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '508a9b3a-e326-4b77-a103-3399cb65f82a'); --Asistencia cursos capacitacion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7'); --Entrada tarde justificada
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'c32eb2eb-882b-4905-8e8f-c03405cee727'); --Justificado Por Autoridad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'aa41a39e-c20e-4cc4-942c-febe95569499'); --Licencia Medica Pre-Natal. Art 106P
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'f7464e86-8b9e-4415-b370-b44b624951ca'); --Receso de Invierno
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'e249bfce-5af3-4d99-8509-9adc2330700b'); --Nacimiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '5289eac5-9221-4a09-932c-9f1e3d099a47'); --Concurso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '68bf4c98-984d-4b71-98b0-4165c69d62ce'); --Licencia medica por maternidad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '30a249d5-f90c-4666-aec6-34c53b62a447'); --Matrimonio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '1c14a13c-2358-424f-89d3-d639a9404579'); --Licencia Sin Goce De Sueldo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '3fb52f24-3eff-4ca2-8133-c7a3abfc7262'); --Justificado Horario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', 'bfaebb07-8d08-4551-b264-85eb4cab6ef1'); --Suspension
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E3', '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9'); --Viaje




INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'e0dfcef6-98bb-4624-ae6c-960657a9a741'); --ausente con aviso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '48773fd7-8502-4079-8ad5-963618abe725'); --Compensatorio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'); --Boleta de Salida
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb'); --Art 102
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'b70013e3-389a-46d4-8b98-8e4ab75335d0'); --Pre-Examen
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a'); --Licencia Anual Ordinaria
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '50998530-10dd-4d68-8b4a-a4b7a87f3972'); --Resolucion 638
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'f9baed8a-a803-4d7f-943e-35c436d5db46'); --Licencia medica corta duracion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'a93d3af3-4079-4e93-a891-91d5d3145155'); --Licencia medica largo tratamiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'b80c8c0e-5311-4ad1-94a7-8d294888d770'); --Licencia medica atencion familiar
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'b309ea53-217d-4d63-add5-80c47eb76820'); --cumple
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '0cd276aa-6d6b-4752-abe5-9258dbfd6f09'); --duelo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b'); --Donacion de Sangre
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'cb2b4583-2f44-4db0-808c-4e36ee059efe'); --Boleta en comision
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '70e0951f-d378-44fb-9c43-f402cbfc63c8'); --ART
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '5c548eab-b8fc-40be-bb85-ef53d594dca9'); --Dia bibliotecario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '508a9b3a-e326-4b77-a103-3399cb65f82a'); --Asistencia cursos capacitacion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7'); --Entrada tarde justificada
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'c32eb2eb-882b-4905-8e8f-c03405cee727'); --Justificado Por Autoridad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'aa41a39e-c20e-4cc4-942c-febe95569499'); --Licencia Medica Pre-Natal. Art 106P
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'f7464e86-8b9e-4415-b370-b44b624951ca'); --Receso de Invierno
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'e249bfce-5af3-4d99-8509-9adc2330700b'); --Nacimiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '5289eac5-9221-4a09-932c-9f1e3d099a47'); --Concurso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '68bf4c98-984d-4b71-98b0-4165c69d62ce'); --Licencia medica por maternidad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '30a249d5-f90c-4666-aec6-34c53b62a447'); --Matrimonio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '1c14a13c-2358-424f-89d3-d639a9404579'); --Licencia Sin Goce De Sueldo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '3fb52f24-3eff-4ca2-8133-c7a3abfc7262'); --Justificado Horario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', 'bfaebb07-8d08-4551-b264-85eb4cab6ef1'); --Suspension
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E4', '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9'); --Viaje





INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'e0dfcef6-98bb-4624-ae6c-960657a9a741'); --ausente con aviso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '48773fd7-8502-4079-8ad5-963618abe725'); --Compensatorio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'); --Boleta de Salida
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb'); --Art 102
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'b70013e3-389a-46d4-8b98-8e4ab75335d0'); --Pre-Examen
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a'); --Licencia Anual Ordinaria
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '50998530-10dd-4d68-8b4a-a4b7a87f3972'); --Resolucion 638
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'f9baed8a-a803-4d7f-943e-35c436d5db46'); --Licencia medica corta duracion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'a93d3af3-4079-4e93-a891-91d5d3145155'); --Licencia medica largo tratamiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'b80c8c0e-5311-4ad1-94a7-8d294888d770'); --Licencia medica atencion familiar
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'b309ea53-217d-4d63-add5-80c47eb76820'); --cumple
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '0cd276aa-6d6b-4752-abe5-9258dbfd6f09'); --duelo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b'); --Donacion de Sangre
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'cb2b4583-2f44-4db0-808c-4e36ee059efe'); --Boleta en comision
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '70e0951f-d378-44fb-9c43-f402cbfc63c8'); --ART
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '5c548eab-b8fc-40be-bb85-ef53d594dca9'); --Dia bibliotecario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '508a9b3a-e326-4b77-a103-3399cb65f82a'); --Asistencia cursos capacitacion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7'); --Entrada tarde justificada
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'c32eb2eb-882b-4905-8e8f-c03405cee727'); --Justificado Por Autoridad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'aa41a39e-c20e-4cc4-942c-febe95569499'); --Licencia Medica Pre-Natal. Art 106P
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'f7464e86-8b9e-4415-b370-b44b624951ca'); --Receso de Invierno
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'e249bfce-5af3-4d99-8509-9adc2330700b'); --Nacimiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '5289eac5-9221-4a09-932c-9f1e3d099a47'); --Concurso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '68bf4c98-984d-4b71-98b0-4165c69d62ce'); --Licencia medica por maternidad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '30a249d5-f90c-4666-aec6-34c53b62a447'); --Matrimonio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '1c14a13c-2358-424f-89d3-d639a9404579'); --Licencia Sin Goce De Sueldo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '3fb52f24-3eff-4ca2-8133-c7a3abfc7262'); --Justificado Horario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', 'bfaebb07-8d08-4551-b264-85eb4cab6ef1'); --Suspension
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E5', '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9'); --Viaje



INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'e0dfcef6-98bb-4624-ae6c-960657a9a741'); --ausente con aviso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '48773fd7-8502-4079-8ad5-963618abe725'); --Compensatorio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'); --Boleta de Salida
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb'); --Art 102
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'b70013e3-389a-46d4-8b98-8e4ab75335d0'); --Pre-Examen
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a'); --Licencia Anual Ordinaria
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '50998530-10dd-4d68-8b4a-a4b7a87f3972'); --Resolucion 638
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'f9baed8a-a803-4d7f-943e-35c436d5db46'); --Licencia medica corta duracion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'a93d3af3-4079-4e93-a891-91d5d3145155'); --Licencia medica largo tratamiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'b80c8c0e-5311-4ad1-94a7-8d294888d770'); --Licencia medica atencion familiar
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'b309ea53-217d-4d63-add5-80c47eb76820'); --cumple
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '0cd276aa-6d6b-4752-abe5-9258dbfd6f09'); --duelo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b'); --Donacion de Sangre
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'cb2b4583-2f44-4db0-808c-4e36ee059efe'); --Boleta en comision
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '70e0951f-d378-44fb-9c43-f402cbfc63c8'); --ART
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '5c548eab-b8fc-40be-bb85-ef53d594dca9'); --Dia bibliotecario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '508a9b3a-e326-4b77-a103-3399cb65f82a'); --Asistencia cursos capacitacion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7'); --Entrada tarde justificada
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'c32eb2eb-882b-4905-8e8f-c03405cee727'); --Justificado Por Autoridad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'aa41a39e-c20e-4cc4-942c-febe95569499'); --Licencia Medica Pre-Natal. Art 106P
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'f7464e86-8b9e-4415-b370-b44b624951ca'); --Receso de Invierno
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'e249bfce-5af3-4d99-8509-9adc2330700b'); --Nacimiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '5289eac5-9221-4a09-932c-9f1e3d099a47'); --Concurso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '68bf4c98-984d-4b71-98b0-4165c69d62ce'); --Licencia medica por maternidad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '30a249d5-f90c-4666-aec6-34c53b62a447'); --Matrimonio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '1c14a13c-2358-424f-89d3-d639a9404579'); --Licencia Sin Goce De Sueldo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '3fb52f24-3eff-4ca2-8133-c7a3abfc7262'); --Justificado Horario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', 'bfaebb07-8d08-4551-b264-85eb4cab6ef1'); --Suspension
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E6', '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9'); --Viaje




INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'e0dfcef6-98bb-4624-ae6c-960657a9a741'); --ausente con aviso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '48773fd7-8502-4079-8ad5-963618abe725'); --Compensatorio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'); --Boleta de Salida
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb'); --Art 102
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'b70013e3-389a-46d4-8b98-8e4ab75335d0'); --Pre-Examen
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a'); --Licencia Anual Ordinaria
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '50998530-10dd-4d68-8b4a-a4b7a87f3972'); --Resolucion 638
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'f9baed8a-a803-4d7f-943e-35c436d5db46'); --Licencia medica corta duracion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'a93d3af3-4079-4e93-a891-91d5d3145155'); --Licencia medica largo tratamiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'b80c8c0e-5311-4ad1-94a7-8d294888d770'); --Licencia medica atencion familiar
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'b309ea53-217d-4d63-add5-80c47eb76820'); --cumple
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '0cd276aa-6d6b-4752-abe5-9258dbfd6f09'); --duelo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b'); --Donacion de Sangre
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'cb2b4583-2f44-4db0-808c-4e36ee059efe'); --Boleta en comision
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '70e0951f-d378-44fb-9c43-f402cbfc63c8'); --ART
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '5c548eab-b8fc-40be-bb85-ef53d594dca9'); --Dia bibliotecario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '508a9b3a-e326-4b77-a103-3399cb65f82a'); --Asistencia cursos capacitacion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7'); --Entrada tarde justificada
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'c32eb2eb-882b-4905-8e8f-c03405cee727'); --Justificado Por Autoridad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'aa41a39e-c20e-4cc4-942c-febe95569499'); --Licencia Medica Pre-Natal. Art 106P
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'f7464e86-8b9e-4415-b370-b44b624951ca'); --Receso de Invierno
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'e249bfce-5af3-4d99-8509-9adc2330700b'); --Nacimiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '5289eac5-9221-4a09-932c-9f1e3d099a47'); --Concurso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '68bf4c98-984d-4b71-98b0-4165c69d62ce'); --Licencia medica por maternidad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '30a249d5-f90c-4666-aec6-34c53b62a447'); --Matrimonio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '1c14a13c-2358-424f-89d3-d639a9404579'); --Licencia Sin Goce De Sueldo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '3fb52f24-3eff-4ca2-8133-c7a3abfc7262'); --Justificado Horario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', 'bfaebb07-8d08-4551-b264-85eb4cab6ef1'); --Suspension
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('E7', '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9'); --Viaje




INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'e0dfcef6-98bb-4624-ae6c-960657a9a741'); --ausente con aviso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', '48773fd7-8502-4079-8ad5-963618abe725'); --Compensatorio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'); --Boleta de Salida
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'b70013e3-389a-46d4-8b98-8e4ab75335d0'); --Pre-Examen
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', '76bc064a-e8bf-4aa3-9f51-a3c4483a729a'); --Licencia Anual Ordinaria
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'f9baed8a-a803-4d7f-943e-35c436d5db46'); --Licencia medica corta duracion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'a93d3af3-4079-4e93-a891-91d5d3145155'); --Licencia medica largo tratamiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'b80c8c0e-5311-4ad1-94a7-8d294888d770'); --Licencia medica atencion familiar
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'b309ea53-217d-4d63-add5-80c47eb76820'); --cumple
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', '0cd276aa-6d6b-4752-abe5-9258dbfd6f09'); --duelo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b'); --Donacion de Sangre
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'cb2b4583-2f44-4db0-808c-4e36ee059efe'); --Boleta en comision
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', '70e0951f-d378-44fb-9c43-f402cbfc63c8'); --ART
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', '5c548eab-b8fc-40be-bb85-ef53d594dca9'); --Dia bibliotecario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', '508a9b3a-e326-4b77-a103-3399cb65f82a'); --Asistencia cursos capacitacion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7'); --Entrada tarde justificada
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'c32eb2eb-882b-4905-8e8f-c03405cee727'); --Justificado Por Autoridad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'aa41a39e-c20e-4cc4-942c-febe95569499'); --Licencia Medica Pre-Natal. Art 106P
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'f7464e86-8b9e-4415-b370-b44b624951ca'); --Receso de Invierno
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'e249bfce-5af3-4d99-8509-9adc2330700b'); --Nacimiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', '5289eac5-9221-4a09-932c-9f1e3d099a47'); --Concurso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', '68bf4c98-984d-4b71-98b0-4165c69d62ce'); --Licencia medica por maternidad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', '30a249d5-f90c-4666-aec6-34c53b62a447'); --Matrimonio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', '1c14a13c-2358-424f-89d3-d639a9404579'); --Licencia Sin Goce De Sueldo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', '3fb52f24-3eff-4ca2-8133-c7a3abfc7262'); --Justificado Horario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', 'bfaebb07-8d08-4551-b264-85eb4cab6ef1'); --Suspension
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Gestion', '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9'); --Viaje




INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', 'e0dfcef6-98bb-4624-ae6c-960657a9a741'); --ausente con aviso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', '48773fd7-8502-4079-8ad5-963618abe725'); --Compensatorio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'); --Boleta de Salida

INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', 'b70013e3-389a-46d4-8b98-8e4ab75335d0'); --Pre-Examen
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', '478a2e35-51b8-427a-986e-591a9ee449d8'); --justificado por medio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', 'b309ea53-217d-4d63-add5-80c47eb76820'); --cumple
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', '0cd276aa-6d6b-4752-abe5-9258dbfd6f09'); --duelo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b'); --Donacion de Sangre
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', 'cb2b4583-2f44-4db0-808c-4e36ee059efe'); --Boleta en comision
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', '5c548eab-b8fc-40be-bb85-ef53d594dca9'); --Dia bibliotecario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', '508a9b3a-e326-4b77-a103-3399cb65f82a'); --Asistencia cursos capacitacion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7'); --Entrada tarde justificada
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', 'c32eb2eb-882b-4905-8e8f-c03405cee727'); --Justificado Por Autoridad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', 'f7464e86-8b9e-4415-b370-b44b624951ca'); --Receso de Invierno
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', 'e249bfce-5af3-4d99-8509-9adc2330700b'); --Nacimiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', '5289eac5-9221-4a09-932c-9f1e3d099a47'); --Concurso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', '30a249d5-f90c-4666-aec6-34c53b62a447'); --Matrimonio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', '3fb52f24-3eff-4ca2-8133-c7a3abfc7262'); --Justificado Horario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Contrato de Obra', '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9'); --Viaje




INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', 'e0dfcef6-98bb-4624-ae6c-960657a9a741'); --ausente con aviso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', '48773fd7-8502-4079-8ad5-963618abe725'); --Compensatorio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'); --Boleta de Salida
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', 'b70013e3-389a-46d4-8b98-8e4ab75335d0'); --Pre-Examen
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', '478a2e35-51b8-427a-986e-591a9ee449d8'); --justificado por medio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', 'b309ea53-217d-4d63-add5-80c47eb76820'); --cumple
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', '0cd276aa-6d6b-4752-abe5-9258dbfd6f09'); --duelo
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b'); --Donacion de Sangre
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', 'cb2b4583-2f44-4db0-808c-4e36ee059efe'); --Boleta en comision
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', '5c548eab-b8fc-40be-bb85-ef53d594dca9'); --Dia bibliotecario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', '508a9b3a-e326-4b77-a103-3399cb65f82a'); --Asistencia cursos capacitacion
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7'); --Entrada tarde justificada
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', 'c32eb2eb-882b-4905-8e8f-c03405cee727'); --Justificado Por Autoridad
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', 'f7464e86-8b9e-4415-b370-b44b624951ca'); --Receso de Invierno
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', 'e249bfce-5af3-4d99-8509-9adc2330700b'); --Nacimiento
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', '5289eac5-9221-4a09-932c-9f1e3d099a47'); --Concurso
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', '30a249d5-f90c-4666-aec6-34c53b62a447'); --Matrimonio
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', '3fb52f24-3eff-4ca2-8133-c7a3abfc7262'); --Justificado Horario
INSERT INTO assistance.positions_justifications (position, justification_id) VALUES ('Beca', '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9'); --Viaje

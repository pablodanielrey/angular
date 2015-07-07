insert into profile.users (id,dni,name,lastname) values ('1','1','admin','admin');
insert into credentials.user_password (id,user_id,username,password) values ('1','1','admin','admin');


/*
  Asistencia
*/
insert into credentials.auth_profile (user_id,profile) values ('1','ADMIN');
insert into credentials.auth_profile (user_id,profile) values ('1','ADMIN-ASSISTANCE');
insert into credentials.auth_profile (user_id,profile) values ('1','ADMIN-OFFICES');

  /*
    oficina donde se asignan los usuarios importados desde los relojes
  */
insert into offices.offices (id,name) values ('45cc065a-7033-4f00-9b19-d7d097129db3','Prolac');


  /*
    Doy permisos de administrador al admin sobre todas las oficinas raiz.
  */

insert into offices.offices_roles (user_id,role,office_id) select '1','autoriza',id from offices.offices o where o.parent is null;
insert into offices.offices_roles (user_id,role,office_id) select '1','realizar-solicitud',id from offices.offices o where o.parent is null;
insert into offices.offices_roles (user_id,role,office_id) select '1','realizar-solicitud-admin',id from offices.offices o where o.parent is null;
insert into offices.offices_roles (user_id,role,office_id) select p.id,'manage-positions',o.id from offices.offices o, profile.users p where o.parent is null and p.dni in ('1');
insert into offices.offices_roles (user_id,role,office_id) select p.id,'admin-office',o.id from offices.offices o, profile.users p where o.parent is null and p.dni in ('1');








insert into assistance.justifications (id,name) values ('76bc064a-e8bf-4aa3-9f51-a3c4483a729a','Licencia Anual Ordinaria');

insert into assistance.justifications (id,name) values ('b309ea53-217d-4d63-add5-80c47eb76820','Cumpleaños');

insert into assistance.justifications (id,name) values ('3d486aa0-745a-4914-a46d-bc559853d367','Incumbencias Climáticas');
insert into assistance.justifications (id,name) values ('478a2e35-51b8-427a-986e-591a9ee449d8','Justificado por Médico');
insert into assistance.justifications (id,name) values ('0cd276aa-6d6b-4752-abe5-9258dbfd6f09','Duelo');
insert into assistance.justifications (id,name) values ('e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b','Donación de Sangre');
insert into assistance.justifications (id,name) values ('70e0951f-d378-44fb-9c43-f402cbfc63c8','ART');
insert into assistance.justifications (id,name) values ('7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7','Entrada Tarde Justificada');
insert into assistance.justifications (id,name) values ('c32eb2eb-882b-4905-8e8f-c03405cee727','Justificado Por Autoridad');
insert into assistance.justifications (id,name) values ('68bf4c98-984d-4b71-98b0-4165c69d62ce','Licencia Médica Por Maternidad');
insert into assistance.justifications (id,name) values ('3fb52f24-3eff-4ca2-8133-c7a3abfc7262','Justificado Horario');
insert into assistance.justifications (id,name) values ('bfaebb07-8d08-4551-b264-85eb4cab6ef1','Suspensión');
insert into assistance.justifications (id,name) values ('7747e3ff-bbe2-4f2e-88f7-9cc624a242a9','Viaje');
insert into assistance.justifications (id,name) values ('1c14a13c-2358-424f-89d3-d639a9404579','Licencia Sin Goce De Sueldo');
insert into assistance.justifications (id,name) values ('508a9b3a-e326-4b77-a103-3399cb65f82a','Asistencia a Congresos/Capacitación');
insert into assistance.justifications (id,name) values ('30a249d5-f90c-4666-aec6-34c53b62a447','Matrimonio');

/*
  Generales
*/
insert into assistance.justifications (id,name) values ('5ec903fb-ddaf-4b6c-a2e8-929c77d8256f','Feriado');
insert into assistance.justifications (id,name) values ('874099dc-42a2-4941-a2e1-17398ba046fc','Paro');

/*
  Tipos de justificaciones por tipo de cargo
*/
insert into assistance.positions_justifications (position, justification_id) select 'Planta Permanente', id as justification_id from assistance.justifications;
insert into assistance.positions_justifications (position, justification_id) select 'Contrato', id as justification_id from assistance.justifications;
insert into assistance.positions_justifications (position, justification_id) select 'Beca', id as justification_id from assistance.justifications;

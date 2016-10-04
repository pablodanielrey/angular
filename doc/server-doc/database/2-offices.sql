create schema offices;

  create table offices.offices (
    id varchar primary key,
    name varchar not null,
    telephone varchar,
    email varchar,
    parent varchar references offices.offices (id),
    constraint unique_office unique (name,parent)
  );

  create table offices.offices_users (
    user_id varchar not null references profile.users (id),
    office_id varchar references offices.offices (id),
    constraint unique_office_user unique (user_id,office_id)
  );


  create table offices.offices_roles (
    user_id varchar not null references profile.users (id),
    office_id varchar references offices.offices (id),
    role varchar not null,
    send_mail boolean default true,
    constraint unique_office_roles unique (user_id,office_id,role)
  );

-- Para migrar de la tablas de assistance al esquema offices solo hay que crear
-- el esquema offices y luego correr las consultas
-- select * into offices.offices from assistance.offices;
-- select * into offices.offices_users from assistance.offices_users;
-- select * into offices.offices_roles from assistance.offices_roles;
-- estas consultas crean las tablas y copian el contenido


/*
Módulo de sistemas.
*/
create schema systems;

create table systems.systems (
  id varchar not null primary key,
  name varchar not null,
  config varchar
);



/*
  Modulo principal de datos del usuario.
*/
create schema profile;

create table profile.users (
    id varchar not null primary key,
    dni varchar not null unique,
    name varchar,
    lastname varchar,
    genre varchar,
    birthdate timestamptz,
    city varchar,
    residence_city varchar,
    country varchar,
    address varchar,
    CHECK(EXTRACT(TIMEZONE FROM birthdate) = '0')
);

create table profile.mails (
    id varchar not null primary key,
    user_id varchar not null references profile.users (id),
    email varchar not null,
    confirmed boolean not null default false,
    hash varchar
);

create table profile.telephones (
    id varchar not null primary key,
    user_id varchar not null references profile.users (id),
    number varchar not null,
    type varchar
);



/*
  Módulo de los grupos.
*/
create schema groups;

create table groups.groups (
    id varchar not null primary key,
    system_id varchar not null references systems.systems (id),
    name varchar not null
);

create table groups.groups_users (
    user_id varchar not null references profile.users (id),
    group_id varchar not null references groups.groups (id),
    constraint primary_key_group_users unique (user_id,group_id)
);



/*
  Módulo de credenciales.
*/
create schema credentials;

create table credentials.user_password (
    id varchar not null primary key,
    user_id varchar not null references profile.users (id),
    username varchar not null unique,
    password varchar not null
);


create table credentials.password_resets (
  user_id varchar not null references profile.users (id),
  username varchar not null,
  creds_id varchar not null references credentials.user_password (id),
  creation timestamptz default now(),
  hash varchar not null primary key,
  executed boolean default false,
  CHECK(EXTRACT(TIMEZONE FROM creation) = '0')
);

create table credentials.auth_profile (
  user_id varchar not null references profile.users (id),
  profile varchar not null
);



/*
  Módulo de requests.
*/
create schema account_requests;

create table account_requests.requests (
    id varchar not null primary key,
    dni varchar not null unique,
    student_number varchar,
    lastname varchar default '',
    name varchar default '',
    email varchar not null,
    reason varchar,
    password varchar not null,
    hash varchar default '',
    confirmed boolean default false,
    created timestamptz default now(),
    CHECK(EXTRACT(TIMEZONE FROM created) = '0')
);



/*
  tablas del módulo de estudiantes.
*/
create schema students;

create table students.users (
  id varchar not null primary key references profile.users (id),
  student_number varchar unique,
  condition varchar
);


/*
  tablas del módulo de au24
*/
create schema au24;

create table au24.users (
  id varchar not null primary key references profile.users (id),
  type varchar
);

/*
tablas del módulo del dominio
*/
create schema domain;

create table domain.users (
  id varchar not null primary key references profile.users (id)
);


/*
tablas del módulo del servidor de correo
*/
create schema mail;

create table mail.users (
  id varchar not null primary key references profile.users (id)
);



/*
  tablas del módulo de inserción laboral
*/
create schema laboral_insertion;

create table laboral_insertion.users (
  id varchar not null primary key references profile.users (id),
  cv bytea,
  reside boolean default false,
  travel boolean default false,
  accepted_conditions boolean default false
);

create table laboral_insertion.languages (
  id varchar not null primary key,
  user_id varchar not null references laboral_insertion.users (id),
  name varchar not null,
  level varchar not null
);

create table laboral_insertion.degree (
  id varchar not null primary key,
  user_id varchar references laboral_insertion.users (id),
  name varchar not null,
  courses integer,
  average1 real,
  average2 real,
  work_type varchar
);


/*
  Tablas del módulo de tutorias
*/

create schema tutors;

create table tutors.tutors (
  id varchar not null primary key,
  user_id varchar references profile.users (id),
  "date" timestamptz not null,
  student_number varchar not null,
  type varchar not null,
  created timestamptz default now(),
  CHECK(EXTRACT(TIMEZONE FROM date) = '0'),
  CHECK(EXTRACT(TIMEZONE FROM created) = '0')
);



/*
  Tablas internas de logs, sesiones, etc. cuestiones internas del sistema van dentro de este esquema.
*/
create schema system;


create table system.logs (
  id serial primary key,
  user_id varchar references profile.users (id),
  creation timestamptz default now(),
  log varchar not null,
  CHECK(EXTRACT(TIMEZONE FROM creation) = '0')
);

create table system.sessions (
  id varchar not null primary key,
  data varchar,
  expire timestamptz default now(),
  CHECK(EXTRACT(TIMEZONE FROM expire) = '0')
);



/*
  Tablas del módulo de asistencia
*/

create schema assistance;


create table assistance.devices (

);

create table assistance.attlog (
    id varchar not null primary key,
    device_id varchar not null,
    user_id varchar not null references profile.users (id),
    verifymode bigint not null,
    log timestamptz not null,
    CHECK(EXTRACT(TIMEZONE FROM log) = '0')
);



create table assistance.positions (
    id varchar primary key,
    user_id varchar not null references profile.users (id),
    name varchar not null
);


create table assistance.schedule (
    id varchar primary key,
    user_id varchar not null references profile.users (id),
    date timestamptz not null,
    sstart timestamptz not null,
    send timestamptz not null,
    isDayOfWeek boolean default true not null,
    isDayOfMonth boolean default false not null,
    isDayOfYear boolean default false not null,
    created timestamptz not null default now(),
    CHECK(EXTRACT(TIMEZONE FROM date) = '0'),
    CHECK(EXTRACT(TIMEZONE FROM sstart) = '0'),
    CHECK(EXTRACT(TIMEZONE FROM send) = '0'),
    CHECK(EXTRACT(TIMEZONE FROM created) = '0')
);

create table assistance.offices (
    id varchar primary key,
    name varchar not null,
    telephone varchar,
    email varchar,
    parent varchar,
    constraint unique_office unique (name,parent)
);

create table assistance.offices_users (
    user_id varchar references profile.users (id),
    office_id varchar references assistance.offices (id)
    contraint unique_office_user unique (user_id,office_id)
);

create table assistance.offices_roles (
  user_id varchar references profile.users (id),
  office_id varchar references assistance.offices (id)
  role varchar not null,
  contraint unique_office_user unique (user_id,office_id,role)
);

create table assistance.justifications (
  id varchar primary key,
  name varchar not null unique
);

create table assistance.justifications_stock (
  justification_id varchar not null references assistance.justifications (id),
  user_id varchar not null references profile.users (id),
  quantity integer not null default 0,
  constraint justifications_stock_unique unique (justification_id, user_id)
);


create table assistance.justifications_requests (
  id varchar primary key,
  user_id varchar not null references profile.users (id),
  justification_id varchar not null references assistance.justifications (id),
  jbegin timestamptz not null,
  jend timestamptz not null,
  status varchar not null,
  CHECK(EXTRACT(TIMEZONE FROM jbegin) = '0'),
  CHECK(EXTRACT(TIMEZONE FROM jend) = '0')
);


/*
  Vistas útiles para buscar usuarios rápido
*/

create schema views;


create or replace view views.users_full_data_with_pass as
  select p.id, p.dni, p.name, p.lastname, c.username, c.password, s.student_number, m.email from profile.users as p
  left outer join credentials.user_password as c on p.id = c.user_id
  left outer join students.users as s on p.id = s.id
  left outer join profile.mails as m on p.id = m.user_id;

create or replace view views.users_full_data as
  select p.id, p.dni, p.name, p.lastname, c.username, s.student_number, m.email from profile.users as p
  left outer join credentials.user_password as c on p.id = c.user_id
  left outer join students.users as s on p.id = s.id
  left outer join profile.mails as m on p.id = m.user_id;

create or replace view views.users_with_pass as
  select p.dni, c.username, c.password, s.student_number, m.email from profile.users as p
  left outer join credentials.user_password as c on p.id = c.user_id
  left outer join students.users as s on p.id = s.id
  left outer join profile.mails as m on p.id = m.user_id;

create or replace view views.users as
  select p.id, p.dni, c.username, s.student_number, m.email, a.type from profile.users as p
  left outer join credentials.user_password as c on p.id = c.user_id
  left outer join students.users as s on p.id = s.id
  left outer join profile.mails as m on p.id = m.user_id
  left outer join au24.users as a on p.id = a.id;

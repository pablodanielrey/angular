
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
    birthdate date,
    city varchar,
    country varchar,
    address varchar
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
    number varchar not null
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
  creation timestamp default now(),
  hash varchar not null primary key,
  executed boolean default false
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
    lastname varchar default '',
    name varchar default '',
    email varchar not null,
    reason varchar,
    password varchar not null,
    hash varchar default '',
    confirmed boolean default false,
    created timestamp default now()
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
  curses integer,
  average1 real,
  average2 real,
  work_type varchar
);



/*
  Tablas internas de logs, sesiones, etc. cuestiones internas del sistema van dentro de este esquema.
*/
create schema system;


create table system.logs (
  id serial primary key,
  user_id varchar references profile.users (id),
  creation timestamp default now(),
  log varchar not null
);

create table system.sessions (
  id varchar not null primary key,
  data varchar,
  expire timestamp default now()
);

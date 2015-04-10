/*
tablas del módulo de inserción laboral
*/
create schema laboral_insertion;

  create table laboral_insertion.users (
    id varchar not null primary key references profile.users (id),
    reside boolean default false,
    travel boolean default false,
    accepted_conditions boolean default false,
    creation timestamptz default now()
  );

  create table laboral_insertion.users_cv (
    id varchar not null primary key references profile.users (id),
    cv bytea,
    creation timestamptz default now()
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

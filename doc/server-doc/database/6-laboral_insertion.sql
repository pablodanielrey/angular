/*
tablas del módulo de inserción laboral
*/
create schema laboral_insertion;

  create table laboral_insertion.users (
    id varchar not null primary key references profile.users (id),
    accepted_conditions boolean default false,
    email varchar references profile.mails (id),
    cv varchar references file.file (id),
    creation timestamptz default now()
  );

  create table laboral_insertion.inscriptions (
    id varchar not null primary key,
    user_id varchar not null references laboral_insertion.users (id),
    reside boolean default false,
    travel boolean default false,
    degree varchar not null,
    courses integer not null,
    average1 real not null,
    average2 real not null,
    work_type varchar not null,
    work_experience boolean default false,
    creation timestamptz default now()
  );

  create table laboral_insertion.languages (
    id varchar not null primary key,
    user_id varchar not null references laboral_insertion.users (id),
    name varchar not null,
    level varchar not null
  );

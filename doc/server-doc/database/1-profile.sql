


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
    version bigint default 0,
    created timestamptz default now()
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

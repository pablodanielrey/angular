create schema ingreso;

create table ingreso.login (
    id serial primary key,
    dni varchar,
    found boolean,
    created timestamp default now()
);

create table ingreso.errors (
    id serial primary key,
    error varchar,
    names varchar,
    dni varchar,
    email varchar,
    comment varchar,
    resolved boolean default false,
    created timestamp default now()
);

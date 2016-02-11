/*
tablas del módulo de manejo de archivos
*/

create schema files;

  create table files.files (
    id varchar not null primary key,
    name varchar,
    hash varchar,
    mimetype varchar default 'application/binary',
    codec varchar default 'base64',
    size bigint default 0,
    content bytea,
    created timestamp default now()
  );

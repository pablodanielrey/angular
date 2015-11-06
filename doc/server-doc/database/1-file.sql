/*
tablas del módulo de manejo de archivos
*/

create schema files;

  create table files.files (
    id varchar not null primary key,
    name varchar,
    hash varchar,
    data bytea
  );

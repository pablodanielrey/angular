/*
tablas del módulo de manejo de archivos
*/

create schema file;

  create table file.file (
    id varchar not null primary key,
    name varchar,
    hash varchar,
    data bytea
  );

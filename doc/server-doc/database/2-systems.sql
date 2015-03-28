/*
Módulo de sistemas.
*/
create schema systems;

  create table systems.systems (
    id varchar not null primary key,
    name varchar not null,
    config varchar
  );

  

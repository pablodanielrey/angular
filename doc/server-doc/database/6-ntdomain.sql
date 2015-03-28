/*
tablas del módulo del dominio
*/
create schema domain;

  create table domain.users (
    id varchar not null primary key references profile.users (id)
  );
  


/*
tablas del módulo de au24
*/
create schema au24;

  create table au24.users (
    id varchar not null primary key references profile.users (id),
    type varchar
  );

  

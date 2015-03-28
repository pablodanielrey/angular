/*
Tablas internas de logs, sesiones, etc. cuestiones internas del sistema van dentro de este esquema.
*/
create schema system;


  create table system.logs (
    id serial primary key,
    user_id varchar,
    creation timestamptz default now(),
    log varchar not null
  );

  create table system.sessions (
    id varchar not null primary key,
    data varchar,
    expire timestamptz default now()
  );

  

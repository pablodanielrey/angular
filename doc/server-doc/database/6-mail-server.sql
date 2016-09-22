
/*
tablas del módulo del servidor de correo
*/
create schema mail;

  create table mail.users (
    id varchar not null primary key references profile.users (id)
  );

  


/*
Tablas del módulo de tutorias
*/

create schema tutors;

  create table tutors.tutors (
    id varchar not null primary key,
    user_id varchar references profile.users (id),
    "date" timestamptz not null,
    student_number varchar not null,
    type varchar not null,
    created timestamptz default now()
  );

  

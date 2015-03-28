

/*
tablas del módulo de estudiantes.
*/
create schema students;

  create table students.users (
    id varchar not null primary key references profile.users (id),
    student_number varchar unique,
    condition varchar
  );
  

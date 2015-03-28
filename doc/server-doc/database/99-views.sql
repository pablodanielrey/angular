

/*
Vistas útiles para buscar usuarios rápido
*/

create schema views;


  create or replace view views.users_full_data_with_pass as
    select p.id, p.dni, p.name, p.lastname, c.username, c.password, s.student_number, m.email from profile.users as p
    left outer join credentials.user_password as c on p.id = c.user_id
    left outer join students.users as s on p.id = s.id
    left outer join profile.mails as m on p.id = m.user_id;

    create or replace view views.users_full_data as
      select p.id, p.dni, p.name, p.lastname, c.username, s.student_number, m.email from profile.users as p
      left outer join credentials.user_password as c on p.id = c.user_id
      left outer join students.users as s on p.id = s.id
      left outer join profile.mails as m on p.id = m.user_id;

      create or replace view views.users_with_pass as
        select p.dni, c.username, c.password, s.student_number, m.email from profile.users as p
        left outer join credentials.user_password as c on p.id = c.user_id
        left outer join students.users as s on p.id = s.id
        left outer join profile.mails as m on p.id = m.user_id;

        create or replace view views.users as
          select p.id, p.dni, c.username, s.student_number, m.email, a.type from profile.users as p
          left outer join credentials.user_password as c on p.id = c.user_id
          left outer join students.users as s on p.id = s.id
          left outer join profile.mails as m on p.id = m.user_id
          left outer join au24.users as a on p.id = a.id;
          

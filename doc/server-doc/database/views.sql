

create or replace view assistance.full_schedule as
  select p.id, p.dni, p.name, p.lastname, s.sstart, s.send from profile.users as p
  left outer join assistance.schedule s on p.id = s.user_id;

  create or replace view assistance.full_office as
    select p.id, p.dni, p.name as username, p.lastname, o.name as officename from profile.users as p, assistance.offices as o, assistance.offices_users as ou
    where ou.user_id = p.id and ou.office_id = o.id;


    create or replace view assistance.full_office_roles as
      select p.id, p.dni, p.name as username, p.lastname, o.name as officename, ou.role from profile.users as p, assistance.offices as o, assistance.offices_roles as ou
      where ou.user_id = p.id and ou.office_id = o.id;

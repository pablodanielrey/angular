


/*
Módulo de los grupos.
*/
create schema groups;

  create table groups.groups (
    id varchar not null primary key,
    system_id varchar not null references systems.systems (id),
    name varchar not null
  );

  create table groups.groups_users (
    user_id varchar not null references profile.users (id),
    group_id varchar not null references groups.groups (id),
    constraint primary_key_group_users unique (user_id,group_id)
  );


  

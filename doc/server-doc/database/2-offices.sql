create schema offices;

  create table offices.offices (
    id varchar primary key,
    name varchar not null,
    telephone varchar,
    email varchar,
    parent varchar,
    constraint unique_office unique (name,parent)
  );

  create table offices.offices_users (
    user_id varchar not null references profile.users (id),
    office_id varchar references offices.offices (id),
    constraint unique_office_user unique (user_id,office_id)
  );


  create table offices.offices_roles (
    user_id varchar not null references profile.users (id),
    office_id varchar references offices.offices (id),
    role varchar not null,
    send_mail boolean default true,
    constraint unique_office_roles unique (user_id,office_id,role)
  );

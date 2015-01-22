

create table users (
    id varchar not null primary key,
    dni varchar not null unique,
    name varchar,
    lastname varchar,
    genre varchar,
    birthdate date,
    city varchar,
    country varchar,
    address varchar
);

create table user_mails (
    id varchar not null primary key,
    user_id varchar not null references users (id),
    email varchar not null,
    confirmed boolean not null default false,
    hash varchar
);

create table user_telephones (
    id varchar not null primary key,
    user_id varchar not null references users (id),
    number varchar not null
);




create table systems (
    id varchar not null primary key,
    name varchar not null,
    config varchar
);




create table groups (
    id varchar not null primary key,
    system_id varchar not null references systems (id),
    name varchar not null
);


create table groups_users (
    user_id varchar not null references users (id),
    group_id varchar not null references groups (id),
    constraint primary_key_group_users unique (user_id,group_id)
);




create table user_password (
    id varchar not null primary key,
    user_id varchar not null references users (id),
    username varchar not null unique,
    password varchar not null
);





create table account_requests (
    id varchar not null primary key,
    dni varchar not null unique,
    lastname varchar,
    name varchar,
    email varchar,
    reason varchar,
    created timestamp default now()
);

create table password_resets (
    user_id varchar not null references users (id),
    username varchar not null,
    creds_id varchar not null references user_password (id),
    creation timestamp default now(),
    hash varchar not null primary key,
    executed boolean default false
);




create table students (
  id varchar not null primary key references users (id),
  student_number varchar unique,
  condition varchar
);



create table logs (
  id serial primary key,
  creation timestamp default now(),
  log varchar not null,
  user_id varchar references users (id)
);


create table sessions (
  id varchar not null primary key,
  data varchar,
  expire timestamp default now()
);

/*
Módulo de credenciales.
*/
create schema credentials;

  create table credentials.user_password (
    id varchar not null primary key,
    user_id varchar not null references profile.users (id),
    username varchar not null unique,
    password varchar not null
  );


  create table credentials.password_resets (
    user_id varchar not null references profile.users (id),
    username varchar not null,
    creds_id varchar not null references credentials.user_password (id),
    creation timestamptz default now(),
    hash varchar not null primary key,
    executed boolean default false,
    CHECK(EXTRACT(TIMEZONE FROM creation) = '0')
  );

  create table credentials.auth_profile (
    user_id varchar not null references profile.users (id),
    profile varchar not null
  );

  

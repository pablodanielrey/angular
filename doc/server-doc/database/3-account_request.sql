

/*
Módulo de requests.
*/
create schema account_requests;

  create table account_requests.requests (
    id varchar not null primary key,
    dni varchar not null unique,
    student_number varchar,
    lastname varchar default '',
    name varchar default '',
    email varchar not null,
    reason varchar,
    password varchar not null,
    hash varchar default '',
    confirmed boolean default false,
    created timestamptz default now(),
    CHECK(EXTRACT(TIMEZONE FROM created) = '0')
  );


  

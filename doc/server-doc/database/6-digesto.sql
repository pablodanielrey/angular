/*
tablas del módulo del digesto
*/
create schema digesto;

  create table digesto.normative (
    id varchar not null primary key,
    issuer_id varchar not null references offices.offices (id),
    file_id varchar references file.file (id),
    type varchar,
    file_number varchar not null,
    normative_number varchar not null,
    date timestamptz,
    created timestamptz default now(),
    creator_id varchar not null references profile.users (id),
    extract text
  );

  create table digesto.related (
    id varchar not null primary key,
    normative_id varchar not null references digesto.normative (id),
    realated_id varchar not null references digesto.normative (id),
    created timestamptz default now(),
    creator_id varchar not null references profile.users (id),
    type varchar
  );

  create table digesto.state_normative (
    id varchar not null primary key,
    state varchar not null,
    created timestamptz default now(),
    creator_id varchar not null references profile.users (id),
    normative_id varchar not null references digesto.normative (id)
  );

  create table digesto.visibility (
    id varchar not null primary key,
    normative_id varchar not null references digesto.normative (id),
    type varchar,
    additional_data varchar
  );

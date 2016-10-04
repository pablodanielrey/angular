

/*
  debe incluirse primero las tablas del sistema

  profile.users
  credentails -- todo el esquema
  system -- todo el esquema
  assistance.devices
  assistance.templates
  assistance.attlog
*/

create table assistance.template_mapping (
  template_id varchar not null references assistance.templates (id),
  user_id varchar not null references profile.users (id),
  reader_index bigint not null,
  created timestamptz default now()
);


create table assistance.sync_user (
  user_id varchar primary key not null references profile.users (id)
);

create table assistance.sync_logs (
  attlog_id varchar primary key not null references assistance.attlog (id)
);

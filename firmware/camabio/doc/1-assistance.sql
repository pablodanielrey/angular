

/*
  debe incluirse primero las tablas del sistema

  profile.users
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

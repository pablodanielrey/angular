create schema assistance;


  create table assistance.devices (

  );

  create table assistance.attlog (
    id varchar not null primary key,
    device_id varchar not null,
    user_id varchar not null references profile.users (id),
    verifymode bigint not null,
    log timestamptz not null,
    created timestamptz default now(),
    CHECK(EXTRACT(TIMEZONE FROM log) = '0')
  );


  create table assistance.positions (
    id varchar primary key,
    user_id varchar not null references profile.users (id),
    name varchar not null
  );


  /*
  para seleccionar el schedule actual es : 2015-02-25 13:00:00-03

  select sstart, send, date from assistance.schedule where
  ((date = '2015-02-25 13:00:00-03'::timestamp) or
  (isDayOfWeek = true and extract(dow from date) = extract(dow from '2015-02-25 13:00:00-03'::timestamp)) or
  (isDayOfMonth = true and extract(day from date) = extract(day from '2015-02-25 13:00:00-03'::timestamp)) or
  (isDayOfYear = true and extract(doy from date) = extract(doy from '2015-02-25 13:00:00-03'::timestamp)))
  order by date desc
  */


  create table assistance.schedule (
    id varchar primary key,
    user_id varchar not null references profile.users (id),
    date timestamptz not null,
    sstart timestamptz not null,
    send timestamptz not null,
    isDayOfWeek boolean default true not null,
    isDayOfMonth boolean default false not null,
    isDayOfYear boolean default false not null,
    created timestamptz not null default now(),
    CHECK(EXTRACT(TIMEZONE FROM date) = '0'),
    CHECK(EXTRACT(TIMEZONE FROM sstart) = '0'),
    CHECK(EXTRACT(TIMEZONE FROM send) = '0')
  );


  create or replace view assistance.full_schedule as
    select p.id, p.dni, p.name, p.lastname, s.sstart, s.send from profile.users as p
    left outer join assistance.schedule s on p.id = s.user_id;


    create table assistance.offices (
      id varchar primary key,
      name varchar not null,
      telephone varchar,
      email varchar,
      parent varchar,
      constraint unique_office unique (name,parent)
    );

    create table assistance.offices_users (
      user_id varchar references profile.users (id),
      office_id varchar references assistance.offices (id),
      constraint unique_office_user unique (user_id,office_id)
    );

    create or replace view assistance.full_office as
      select p.id, p.dni, p.name as username, p.lastname, o.name as officename from profile.users as p, assistance.offices as o, assistance.offices_users as ou
      where ou.user_id = p.id and ou.office_id = o.id;


    create table assistance.offices_roles (
      user_id varchar references profile.users (id),
      office_id varchar references assistance.offices (id),
      role varchar not null,
      constraint unique_office_roles unique (user_id,office_id,role)
    );

    create or replace view assistance.full_office_roles as
      select p.id, p.dni, p.name as username, p.lastname, o.name as officename, ou.role from profile.users as p, assistance.offices as o, assistance.offices_roles as ou
      where ou.user_id = p.id and ou.office_id = o.id;


    create table assistance.justifications (
      id varchar primary key,
      name varchar not null unique
    );

    create table assistance.justifications_stock (
      justification_id varchar not null references assistance.justifications (id),
      user_id varchar not null references profile.users (id),
      stock integer not null default 0,
      constraint justifications_stock_unique unique (justification_id, user_id)
    );



    /*
    pedidos de justificaciones
    el estado puede ser :

    status = APROVED | REJECTED | PENDING | CANCELED

    */

    create table assistance.justifications_requests (
      id varchar primary key,
      user_id varchar not null references profile.users (id),
      justification_id varchar not null references assistance.justifications (id),
      jbegin timestamptz not null,
      jend timestamptz not null,
      created timestamptz not null default now(),
      CHECK(EXTRACT(TIMEZONE FROM jbegin) = '0'),
      CHECK(EXTRACT(TIMEZONE FROM jend) = '0'))
    );


    create table assistance.justifications_requests_status (
      request_id varchar not null references assistance.justifications_requests (id),
      user_id varchar not null references profile.users (id),
      status varchar not null,
      created timestamptz not null default now()
    );

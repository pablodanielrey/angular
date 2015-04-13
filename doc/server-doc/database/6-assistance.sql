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


  create table assistance.users (
    id varchar not null references profile.users (id),
    created timestamptz default now(),
    UNIQUE(id)
  );

  create table assistance.positions (
    id varchar primary key,
    user_id varchar not null references assistance.users (id),
    name varchar not null
  );


  create table assistance.schedule_checks (
    user_id varchar not null references assistance.users (id),
    check_from timestamptz not null,
    enable boolean not null default true,
    created timestamptz default now(),
    CHECK(EXTRACT(TIMEZONE FROM check_from) = '0')
  );

  create table assistance.schedule (
    id varchar primary key,
    user_id varchar not null references assistance.users (id),
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


    create table assistance.offices (
      id varchar primary key,
      name varchar not null,
      telephone varchar,
      email varchar,
      parent varchar,
      constraint unique_office unique (name,parent)
    );

    create table assistance.offices_users (
      user_id varchar not null references assistance.users (id),
      office_id varchar references assistance.offices (id),
      constraint unique_office_user unique (user_id,office_id)
    );


    create table assistance.offices_roles (
      user_id varchar not null references assistance.users (id),
      office_id varchar references assistance.offices (id),
      role varchar not null,
      constraint unique_office_roles unique (user_id,office_id,role)
    );

    create table assistance.justifications (
      id varchar primary key,
      name varchar not null unique
    );

    create table assistance.justifications_stock (
      justification_id varchar not null references assistance.justifications (id),
      user_id varchar not null references assistance.users (id),
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
      user_id varchar not null references assistance.users (id),
      justification_id varchar not null references assistance.justifications (id),
      jbegin timestamptz not null,
      jend timestamptz,
      created timestamptz not null default now(),
      CHECK(EXTRACT(TIMEZONE FROM jbegin) = '0')
    );


    create table assistance.justifications_requests_status (
      request_id varchar not null references assistance.justifications_requests (id),
      user_id varchar not null references assistance.users (id),
      status varchar not null,
      created timestamptz not null default now()
    );



    create table assistance.overtime_requests (
      id varchar primary key,
      user_id varchar not null references assistance.users (id),
      requestor_id varchar not null references assistance.users (id),
      jbegin timestamptz not null,
      jend timestamptz,
      reason varchar not null,
      created timestamptz not null default now(),
      CHECK(EXTRACT(TIMEZONE FROM jbegin) = '0')
    );


    create table assistance.overtime_requests_status (
      request_id varchar not null references assistance.overtime_requests (id),
      user_id varchar not null references assistance.users (id),
      status varchar not null,
      created timestamptz not null default now()
    );

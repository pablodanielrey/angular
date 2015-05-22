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


  create table assistance.status (
    id varchar not null,
    user_id varchar not null references profile.users (id),
    enabled boolean not null,
    date timestamptz default now()
  );

  create table assistance.positions (
    id varchar primary key,
    user_id varchar not null references profile.users (id),
    name varchar not null
  );


  /*
    define si se hace el chequeo o no.
    los tipos de chequeo son mutualmente excluyentes y pueden ser:
    PRESENCE | HOURS | SCHEDULE

    NULL = no se chequea nada
    PRESENCE = que marque una sola vez dentro del horario del schedule
    HOURS = no importa el horario si no que cumplan en el día la cantidad de horas
    SCHEDULE = que cumplan el horario
  */
  create table assistance.checks (
    id varchar primary key,
    user_id varchar not null references profile.users (id),
    date timestamptz not null,
    enable boolean not null default true,
    type varchar not null,
    created timestamptz default now(),
    CHECK(EXTRACT(TIMEZONE FROM date) = '0')
  );

  create table assistance.hours_check (
    id varchar primary key references assistance.checks (id),
    count int default 0
  );


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


  create table assistance.offices (
    id varchar primary key,
    name varchar not null,
    telephone varchar,
    email varchar,
    parent varchar,
    constraint unique_office unique (name,parent)
  );

  create table assistance.offices_users (
    user_id varchar not null references profile.users (id),
    office_id varchar references assistance.offices (id),
    constraint unique_office_user unique (user_id,office_id)
  );


  create table assistance.offices_roles (
    user_id varchar not null references profile.users (id),
    office_id varchar references assistance.offices (id),
    role varchar not null,
    send_mail boolean default true,
    constraint unique_office_roles unique (user_id,office_id,role)
  );

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

    --------------------------------------------------------------------------

    agregar la columna requestor_id con el valor por defecto del user_id

    set timezone to utc;
    begin;
    alter table assistance.justifications_requests add column requestor_id varchar references profile.users (id);
    update assistance.justifications_requests set requestor_id = user_id;
    end;

    */

    create table assistance.justifications_requests (
      id varchar primary key,
      user_id varchar not null references profile.users (id),
      requestor_id varchar not null references profile.users (id),
      justification_id varchar not null references assistance.justifications (id),
      jbegin timestamptz not null,
      jend timestamptz,
      created timestamptz not null default now(),
      CHECK(EXTRACT(TIMEZONE FROM jbegin) = '0')
    );


    create table assistance.justifications_requests_status (
      request_id varchar not null references assistance.justifications_requests (id),
      user_id varchar not null references profile.users (id),
      status varchar not null,
      created timestamptz not null default now()
    );


    create table assistance.general_justifications (
      id varchar primary key,
      justification_id varchar not null references assistance.justifications (id),
      jbegin timestamptz not null,
      jend timestamptz,
      created timestamptz not null default now(),
      CHECK(EXTRACT(TIMEZONE FROM jbegin) = '0')
    );



    create table assistance.overtime_requests (
      id varchar primary key,
      user_id varchar not null references profile.users (id),
      requestor_id varchar not null references profile.users (id),
      jbegin timestamptz not null,
      jend timestamptz,
      reason varchar not null,
      created timestamptz not null default now(),
      CHECK(EXTRACT(TIMEZONE FROM jbegin) = '0')
    );


    create table assistance.overtime_requests_status (
      request_id varchar not null references assistance.overtime_requests (id),
      user_id varchar not null references profile.users (id),
      status varchar not null,
      created timestamptz not null default now()
    );

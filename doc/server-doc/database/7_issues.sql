
CREATE SCHEMA issues;

  CREATE TABLE issues.request (
    id VARCHAR NOT NULL PRIMARY KEY,
    created TIMESTAMPTZ NOT NULL default now(),
  	request TEXT ,
    requestor_id VARCHAR NOT NULL REFERENCES profile.users (id),
    office_id VARCHAR NOT NULL REFERENCES offices.offices (id),
    related_request_id VARCHAR REFERENCES issues.request (id),
    assigned_id VARCHAR REFERENCES profile.users (id),
    priority INTEGER NOT NULL default 0
  );

  CREATE TABLE issues.state (
    created TIMESTAMPTZ NOT NULL default now(),
	  state VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL REFERENCES profile.users (id),
    request_id VARCHAR NOT NULL REFERENCES issues.request (id)
  );

  CREATE TABLE issues.visibility_group_owner (
    id VARCHAR NOT NULL PRIMARY KEY,
    request_id VARCHAR NOT NULL REFERENCES issues.request(id),
    office_id VARCHAR NOT NULL REFERENCES offices.offices (id),
    created TIMESTAMPTZ NOT NULL default now(),
    tree boolean default true
  );

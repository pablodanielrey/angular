
CREATE SCHEMA issues;

  CREATE TABLE issues.request (
    id VARCHAR NOT NULL PRIMARY KEY,
    created TIMESTAMPTZ NOT NULL default now(),
  	request TEXT NOT NULL,
    requestor_id VARCHAR NOT NULL REFERENCES profile.users (id),
    office_id VARCHAR NOT NULL REFERENCES offices.offices (id),
    related_request_id VARCHAR REFERENCES issues.request (id),
    priority INTEGER NOT NULL default 0,
    visibility VARCHAR default 'AUTHENTICATED'
  );

  CREATE TABLE issues.state (
    created TIMESTAMPTZ NOT NULL default now(),
	  state VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL REFERENCES profile.users (id),
    request_id VARCHAR NOT NULL REFERENCES issues.request (id)
  );


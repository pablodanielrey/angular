
CREATE SCHEMA task;

  CREATE TABLE task.task (
    id VARCHAR NOT NULL PRIMARY KEY,
    created TIMESTAMPTZ NOT NULL default now(),
    description TEXT ,
    user_id VARCHAR REFERENCES profile.users (id),
    finish boolean default false
  );

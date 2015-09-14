
CREATE SCHEMA camera;

  CREATE TABLE camera.camera (
    id VARCHAR NOT NULL PRIMARY KEY,
    mac VARCHAR,
    ip VARCHAR,
    floor VARCHAR,
    number INTEGER
  );

  CREATE TABLE camera.recording (
    id VARCHAR NOT NULL PRIMARY KEY,
    fps decimal,
    source VARCHAR,
    start timestamptz NOT NULL,
    rend timestamptz NOT NULL,
    size VARCHAR NOT NULL,
    file_name VARCHAR,
    camera_id VARCHAR REFERENCES camera.camera (id)
  );


DELETE FROM assistance.schedule WHERE EXTRACT(EPOCH FROM (send - date)) <= 0 OR EXTRACT(EPOCH FROM (sstart - date)) <= 0;

CREATE TABLE scheduleTemp (
    id varchar primary key,
    user_id varchar not null,
    sdate date not null,
    sstart bigint not null,
    send bigint not null,
    isDayOfWeek boolean default true not null,
    isDayOfMonth boolean default false not null,
    isDayOfYear boolean default false not null,
    created timestamptz not null default now()
);


INSERT INTO scheduleTemp(id, user_id, sdate, sstart, send, isDayOfWeek, isDayOfMonth, isDayOfYear, created) SELECT 
  id, 
  user_id, 
  date::date, 
  EXTRACT(EPOCH FROM (sstart - date)), 
  EXTRACT(EPOCH FROM (send - date)),
  isDayOfWeek,
  isDayOfMonth,
  isDayOfYear,
  created
  FROM assistance.schedule;


ALTER TABLE assistance.schedule ADD sdate DATE;
ALTER TABLE assistance.schedule DROP date;
ALTER TABLE assistance.schedule DROP sstart;
ALTER TABLE assistance.schedule ADD sstart BIGINT;
ALTER TABLE assistance.schedule DROP send;
ALTER TABLE assistance.schedule ADD send BIGINT;

DELETE FROM assistance.schedule;

INSERT INTO assistance.schedule (id,user_id,sdate,sstart,send, isDayOfWeek, isDayOfMonth, isDayOfYear, created)
SELECT id, user_id, sdate, sstart, send, isDayOfWeek, isDayOfMonth, isDayOfYear, created 
FROM scheduleTemp;

DROP TABLE scheduleTemp;

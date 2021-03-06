ALTER TABLE assistance.checks ADD sdate date;

ALTER TABLE assistance.checks DROP CONSTRAINT checks_date_check;


UPDATE assistance.checks c
SET sdate = s.date
FROM (
  SELECT id, date::date  AS date
  FROM assistance.checks
) AS s
WHERE c.id = s.id;


ALTER TABLE assistance.checks DROP date;



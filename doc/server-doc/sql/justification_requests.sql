SELECT * FROM assistance.justifications_requests jr 
INNER JOIN assistance.justifications_requests_status jrs ON (jr.id = jrs.request_id) 
WHERE jr.user_id = '35f7a8a6-d844-4d6f-b60b-aab810610809' 
AND lower(status) = 'approved' AND jbegin >= '2015-07-01' AND jbegin <= '2015-08-01';


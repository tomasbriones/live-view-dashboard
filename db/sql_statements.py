SELECT_PUBLIC_SERVICE = """
select 
prs.id, prs.permit_id, 
pp.permit_id as chile_atiende_id, 
pp.title, prs.stage as stage_code, prbs.code as status_code, 
prbs.name as status, prs.description
from permit_requests_basepermitrequeststatus prbs
join permit_requests_permitrequeststatus prs on prs.base_status_id = prbs.id 
join permits_permit pp on prs.permit_id = pp.id 
where pp.public_service_id = 106
order by 3;
select 
prs.id, prs.permit_id, 
pp.permit_id as chile_atiende_id, 
pp.title, prs.stage as stage_code, prbs.code as status_code, 
prbs.name as status, prs.description
from permit_requests_basepermitrequeststatus prbs
join permit_requests_permitrequeststatus prs on prs.base_status_id = prbs.id 
join permits_permit pp on prs.permit_id = pp.id 
where pp.permit_id = 16583
order by prs.stage, prbs.code;
select 
pp.permit_id,
err.stage_code, 
err.status_code, 
err.status, 
err.response_error,
count(*) as total
from
permit_requests_permitrequest pr
join permits_permit pp on pp.id = pr.permit_id 
join (
	select
	cast(split_part(url, '/', 5) as integer) as application_id, 
	request_data->>'stage_code' as stage_code, 
	request_data->>'status_code' as status_code, 
	request_data->>'status' as status,
	response_data->>'message' as response_error
	from logs_apirequestlog 
	where public_service_id = 106 
	and url <>'/api/v1/api-token-auth/' 
	and request_data->>'status' <> 'Trámite Pagado vìa web'
	and response_data->>'status' = 'ERROR'
	and (
		response_data::text = '{"status": "ERROR", "message": "No se encontró ningún estado para el permiso, etapa, y status_code ingresados"}'
		or response_data::text = '{"status": "ERROR", "message": "No status found with that status_code, status, stage_code and permit"}'
		or response_data::text = '{"status": "ERROR", "message": "No status found with that status code, status, stage_code and permit"}'
	)
) err on err.application_id = pr.id
group by 1,2,3,4,5 
order by 6 desc
LIMIT 2;
"""


SELECT_URL_REQ_RES_LOG = """
select
err.created_at,
pp.permit_id,
url,
err.ms_application_id,
err.response_error,
err.request_data,
err.id as api_req_log_id
from
permit_requests_permitrequest pr
join permits_permit pp on pp.id = pr.permit_id 
join (
	select
	lar.id,
	cast(split_part(lar.url, '/', 5) as integer) as ms_application_id,
	lar.url as url,
	lar.request_data,
	lar.response_data->>'message' as response_error,
	lar.created_at
	from logs_apirequestlog lar
  	where public_service_id = 106 
	and url <>'/api/v1/api-token-auth/' 
	and request_data->>'status' <> 'Trámite Pagado vìa web' 
	and response_data->>'status' = 'ERROR'
	and (
		response_data::text = '{"status": "ERROR", "message": "No se encontró ningún estado para el permiso, etapa, y status_code ingresados"}'
		or response_data::text = '{"status": "ERROR", "message": "No status found with that status_code, status, stage_code and permit"}'
		or response_data::text = '{"status": "ERROR", "message": "No status found with that status code, status, stage_code and permit"}'
	)
) err on err.ms_application_id = pr.id
and pp.permit_id = 16583;
"""

CREATE_TABLE_PATCHES_LOGS = """
create table api_patches_logs (
	id SERIAL NOT NULL PRIMARY KEY,
	request JSON NOT NULL,
	url VARCHAR(100) NOT NULL,
	log_created_at timestamp with time zone,
	status VARCHAR(25) NOT NULL,
	counter INT NOT NULL,
	ms_application_id INT NOT NULL,
	created_at timestamp with time zone,
	date_updated INT NOT NULL DEFAULT 0,
	original_log_id INT NOT NULL DEFAULT 0
);
"""

INSERT_DATA_IN_PATCHES_LOGS = """
	INSERT INTO api_patches_logs (
		request, 
		url, 
		log_created_at, 
		status, 
		counter, 
		ms_application_id, 
		created_at,
		original_log_id
	) VALUES (
		'%s','%s','%s','PENDING', 0, '%s', CURRENT_TIMESTAMP,'%s'
	);
"""

SELECT_PATCHES_LOGS_REQ_URL = """
	SELECT id, request, url, created_at FROM api_patches_logs WHERE status = 'PENDING';
"""

UPDATE_PATCHES_LOGS_STATUS = """
	UPDATE api_patches_logs SET status = '%s' where id = %s;
"""

SELECT_PATCHES_LOGS_ID = """
	SELECT counter FROM api_patches_logs where id = %s;
"""

UPDATE_PATCHES_LOGS_COUNTER = """
	UPDATE api_patches_logs SET counter = %s where id = %s;
"""

GET_PERMIT_ORIGINAL_DATE = """
	SELECT log_created_at from api_patches_logs where status = 'OK'	and created_at = '%s' and ms_application_id = %s limit 1;
"""

GET_CHANGE_STATE_DATE_NOTIFICATION = """	
	SELECT * from notifications_notification where permit_request_id = %s order by created_at desc limit 1;
"""

UPDATE_CHANGE_STATE_DATE_NOTIFICATION = """
	UPDATE notifications_notification SET created_at = '%s', updated_at = '%s' where created_at in (select created_at from notifications_notification where created_at between '%s' and now() and permit_request_id = %s order by created_at asc limit 1);
"""

SELECT_ORIGINAL_API_LOGS_ID = """
	SELECT EXISTS (SELECT original_log_id FROM public.api_patches_logs WHERE original_log_id = %s );
"""

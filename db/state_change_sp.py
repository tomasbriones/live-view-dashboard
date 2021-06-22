STATE_CHANGE = """
CREATE OR REPLACE FUNCTION create_permit_status(
stage_code text, status_code text, status_name text, 
status_description text, chile_atiende_permit_id int)
RETURNS INTEGER
AS $$
declare
	permits_permit_id INTEGER;
	base_status_id INTEGER;
	status_id INTEGER;
begin
	-- Comprobamos que existe el chile_atiende_permit_id
	-- Para el insert se usa el id, no el permit_id de la tabña permits_permit
	SELECT permits_permit.id FROM permits_permit WHERE permit_id = chile_atiende_permit_id
	into permits_permit_id;
	IF NOT FOUND THEN
		RAISE EXCEPTION 'El trámite % no existe', chile_atiende_permit_id;
	END IF;
  	-- Comprobamos que no hay estados como el que se indica con ese permit_id
	PERFORM 1 from permit_requests_basepermitrequeststatus prbs
	join permit_requests_permitrequeststatus prs on prs.base_status_id = prbs.id 
	join permits_permit pp on prs.permit_id = pp.id 
	where pp.permit_id = chile_atiende_permit_id 
	and prbs.code = status_code
	and prbs.name = status_name
	and prs.stage = stage_code;
	IF FOUND THEN
		RAISE EXCEPTION 'El estado para ese trámite ya existe';
	end if;
  -- Encontramos el base_status_id, si no lo creamos
	SELECT permit_requests_basepermitrequeststatus.id FROM permit_requests_basepermitrequeststatus WHERE name = status_name AND code = status_code
	INTO base_status_id;
	IF NOT FOUND THEN
		RAISE NOTICE 'Creating new base_status "%"/"%"', status_name, status_code;
		INSERT INTO permit_requests_basepermitrequeststatus (name,created_at, code,fa_icon,icon_color) 
		VALUES (status_name, now(), status_code, 'fa-times', '000000')
		RETURNING id into base_status_id;
	ELSE
		RAISE NOTICE 'base_status "%"/"%" already created', status_name, status_code;
	END IF;
	INSERT INTO permit_requests_permitrequeststatus (created_at, permit_id, stage, description, base_status_id) 
	VALUES (now(), permits_permit_id, stage_code, status_description, base_status_id)
	RETURNING id into status_id;
	RAISE NOTICE 'Nuevo estado creado, status_id: %', status_id;
	RETURN status_id;
END;
$$
LANGUAGE plpgsql;
"""
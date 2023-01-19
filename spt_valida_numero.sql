CREATE OR REPLACE PROCEDURE public.stp_valida_numero() AS $$
DECLARE
r RECORD;
BEGIN
FOR r IN
select t.numero, date_part('day', timestamp 'now()') - date_part('day', t.fecha_seleccionado) as dia from public.rifa_numeros t where t.fecha_seleccionado is not null and t.fecha_pagado is null
LOOP
if r.dia > 1 then
update public.rifa_numeros set fecha_seleccionado = null, seleccionado = false, participante = null where numero = r.numero;
end if;
END LOOP;
exception
when no_data_found then
raise exception 'Datos % no encontrados',r.dia;
END;
$$ LANGUAGE 'plpgsql';
ALTER PROCEDURE public.stp_valida_numero() OWNER TO rifasuser;

insert into current_weather_conditions 
select 
rcw.id as current_weather_id,
rcw.ingestion_timestamp_utc,
rec.id as weather_id,
rec.main,
rec.description,
rec.icon
from 
  raw_current_weather rcw
  left join current_weather_conditions cwc on rcw.id = cwc.current_weather_id  ,
  jsonb_to_recordset(raw_data->'weather') as rec(id int, main varchar(255), description varchar(255), icon varchar(255))
where 
	cwc.current_weather_id is null
;

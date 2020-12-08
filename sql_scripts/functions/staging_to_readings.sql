CREATE OR REPLACE FUNCTION to_int(i varchar) 
RETURNS int AS $$			  		
	BEGIN	
	return
	CASE WHEN i~E'^\\d+$' THEN CAST (i AS INTEGER)	ELSE null END;	
	END;			
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION to_float(txt varchar) 
RETURNS float AS $$			  		
	BEGIN	
		return txt::float;
	exception
		when others then
		return null;
	END;			
$$ LANGUAGE plpgsql;


DROP FUNCTION to_ts(character varying,character varying);
CREATE OR REPLACE FUNCTION to_ts(txt varchar,f varchar) 
RETURNS timestamp AS $$			  		
	BEGIN	
		return to_timestamp(txt,f);
	exception
		when others then
		return null;
	END;			
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION staging_to_readings(rn varchar) 
RETURNS void AS $$			  		
	Declare s int=(select f_line+2 from staging where r='<RESULTS>');
			dt varchar=Split_part(r,',',19) from staging where f_line=3;
			
	BEGIN
		insert into run_info(run,survey_date) values (rn,to_date(dt,'dd/mm/yyyy'));
										
		insert into readings(run,f_line,ch,left_skid,lat,lon,alt,ts)
		select 
		rn
		,f_line
		,to_int(Split_part(r,',',1)) as ch
		,to_float(Split_part(r,',',2)) as left_skid
		,to_float(Split_part(r,',',8)) as lat
		,to_float(Split_part(r,',',9)) as lon
		,to_float(Split_part(r,',',10)) as alt
		,to_ts('01/10/2020'||'/'||Split_part(r,',',13),'dd/mm/yyyy/HH24:MI:ss') as ts
		from staging where f_line>=s;
	
		update readings set pt=ST_transform(ST_SetSRID(ST_makePoint(lon,lat),4326),27700) where run=rn;
		--interpolating readings					 
		update readings set pt=last_pt(rn,f_line) where run=rn and pt is null;

		PERFORM interpolate_readings(rn,rg) from 
			(select pt,unnest(array_cluster(array_agg(f_line),1)) as rg,array_agg(f_line) from readings where run=rn group by pt having count(f_line)>1) a
		where upper(rg)-1>lower(rg);--more than 1 point
		 
		delete from staging;
							  
	END;			
$$ LANGUAGE plpgsql;


--delete from readings;
--delete from run_info where run='staging';
--select staging_to_readings('staging');										
										
--select * from readings where pt is null;
--update readings set vect=st_makeline(a.pt,next_pt) from 
--(select run,f_line,pt,lead(pt) over(partition by run order by f_line) as next_pt from readings) a
--where a.run=readings.run and a.f_line=readings.f_line
--;


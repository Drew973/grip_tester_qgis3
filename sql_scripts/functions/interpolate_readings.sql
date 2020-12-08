set search_path to gtest,public;

--find nect
CREATE OR REPLACE FUNCTION next_pt(rn varchar,l int)
RETURNS geometry AS $$		

	declare p geometry=pt from readings where run=rn and f_line=l;
	BEGIN
	if p is null then
		return (select pt from readings where run=rn and f_line>l and not pt is null order by f_line limit 1);
	else
		return (select pt from readings where run=rn and f_line>l and not (st_equals(p,pt) or pt is null) order by f_line limit 1);
	end if;
	END;			
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION last_pt(rn varchar,l int)
RETURNS geometry AS $$		

	declare p geometry=pt from readings where run=rn and f_line=l;
	BEGIN	
	if p is null then
		return (select pt from readings where run=rn and f_line<l and not pt is null order by f_line desc limit 1);
	else
		return (select pt from readings where run=rn and f_line<l and not (st_equals(p,pt) or pt is null) order by f_line desc limit 1);
	end if;
	END;			
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION ch_fraction(c float,s float,e float) 
RETURNS float AS $$			  		
	BEGIN
	
		if e=s then
			return null;
		else
			return (c-s)/(e-s);
		end if;
	END;			
$$ LANGUAGE plpgsql;


--interpolate readings in run rn with f_line in range rg. Sets pt between 1st point and next point.

--uppper(rg)-1 can = lower(rg) 
--rg is range of f_line
CREATE OR REPLACE FUNCTION interpolate_readings(rn varchar,rg int4range)
RETURNS void AS $$		

	declare
		s int=lower(rg);
		e int =upper(rg)-1;
		g geometry=st_makeLine((select pt from readings where run=rn and f_line=lower(rg)),next_pt(rn,lower(rg)));--line from point to next point.
	BEGIN
		if g is null then
			raise NOTICE 'null geometry';
		end if;
		
		if s=e then
			raise exception 'interpolate readings s=e=%',s;
		end if;			
																																																
		update readings set pt=st_lineinterpolatepoint(g,ch_fraction(f_line,s,e)) where run=rn and f_line<@rg;
	END;			
$$ LANGUAGE plpgsql;


update readings set pt=ST_transform(ST_SetSRID(ST_makePoint(lon,lat),4326),27700);
update readings set pt=last_pt(run,f_line) where pt is null;


with a as (select run,pt,unnest(array_cluster(array_agg(f_line),1)) as rg,array_agg(f_line) from readings group by run,pt having count(f_line)>1)
	select interpolate_readings(run,rg) from a 
	where upper(rg)-1>lower(rg);--more than 1 point
	
;							
select * from readings where pt is null;

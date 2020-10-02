CREATE OR REPLACE FUNCTION gtest.update_readings(rn varchar) 
	RETURNS void AS $$
	
	BEGIN
		with a as (select f_line,run,pt,lead(pt) over(partition by run order by f_line) as np from gtest.readings)
		update gtest.readings as r set vect=st_makeline(a.pt,np) from a where a.run=r.run and a.f_line=r.f_line and r.run=rn ;--can't directly use lead/lag in update

	with b as (select f_line,run,pt,lag(pt) over(partition by run order by f_line) as lp from gtest.readings)
		update gtest.readings as r set vect=st_makeline(lp,b.pt) from b where vect is null and b.run=r.run and b.f_line=r.f_line and r.run=rn;													  
	END;			
$$ LANGUAGE plpgsql;
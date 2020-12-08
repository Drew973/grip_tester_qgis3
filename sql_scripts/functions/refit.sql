SET SEARCH_PATH TO GTEST,PUBLIC;

CREATE OR REPLACE FUNCTION interpolate_chainage(chainage float, rn varchar,sl int,el int,start_sec_ch float,end_sec_ch float) 
	RETURNS float AS $$
	declare
	x1 float=(select ch from readings where run=rn and f_line=sl);
	x2 float=(select ch from readings where run=rn and f_line=el);
	
	BEGIN
	return interpolate(chainage,x1,start_sec_ch,x2,end_sec_ch);																  
	END;			
$$ LANGUAGE plpgsql;


drop function if exists gtest.refit_all();

CREATE OR REPLACE FUNCTION gtest.refit() 
	RETURNS void AS $$
	
	BEGIN
	delete from gtest.fitted;
	
	insert into gtest.fitted
	select routes.run,ch,reversed,left_skid as gn,f_line,speed,pt,vect,sec,xsp,
	
	case when start_sec_ch>=0 and end_sec_ch>=0 then interpolate_chainage(ch,readings.run,s_line,e_line,start_sec_ch,end_sec_ch)
	else
	meas_sec_ch(sec,pt)
	end
	as sec_ch
		
	from readings inner join routes 
	on routes.run=readings.run and s_line<=f_line and f_line<=e_line;
	 																				  
	END;			
$$ LANGUAGE plpgsql;

alter function gtest.refit() set search_path=gtest,public;


CREATE OR REPLACE FUNCTION gtest.refit(rn varchar) 
	RETURNS void AS $$
	
	BEGIN
	delete from gtest.fitted where run=rn;
	
	insert into gtest.fitted
	select routes.run,ch,reversed,left_skid as gn,f_line,speed,pt,vect,sec,xsp,
	
	case when start_sec_ch>=0 and end_sec_ch>=0 then interpolate_chainage(ch,readings.run,s_line,e_line,start_sec_ch,end_sec_ch)
	else
	meas_sec_ch(sec,pt)
	end
	as sec_ch
		
	from readings inner join routes 
	on routes.run=rn and readings.run=rn and s_line<=f_line and f_line<=e_line;
	 																				  
	END;			
$$ LANGUAGE plpgsql;




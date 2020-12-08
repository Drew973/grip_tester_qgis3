SET SEARCH_PATH TO GTEST,PUBLIC;

CREATE OR REPLACE FUNCTION gtest.resize_all() 
	RETURNS void AS $$
	
	BEGIN
	
	delete from gtest.resized;

	insert into gtest.resized(sec,reversed,xsp,s_ch,e_ch,pks,geom)
	select pieces.sec,pieces.reversed,pieces.xsp,s_ch,e_ch,array_agg(pk) as pks,geom
	from gtest.pieces as pieces left join gtest.fitted as fitted on fitted.sec=pieces.sec and fitted.xsp=pieces.xsp and fitted.reversed=pieces.reversed and s_ch<=sec_ch and sec_ch<=e_ch
	group by pieces.sec,pieces.reversed,pieces.xsp,s_ch,e_ch,geom;
																		  
	END;			
$$ LANGUAGE plpgsql;
																								
												
--updates resized where no data by looking for readings with sec_ch within tol.
CREATE OR REPLACE FUNCTION gtest.find_nearby(tol float=10) 
	RETURNS void AS $$
	
	BEGIN
	update gtest.resized set pks=array( select pk from gtest.fitted as f where f.sec=resized.sec and f.xsp=resized.xsp and f.reversed=resized.reversed and s_ch-tol<=sec_ch and sec_ch<=e_ch+tol) where empty_or_null(pks);
	--pks is {null} where no readings
	END;			
$$ LANGUAGE plpgsql;
																																

																								
																								
CREATE OR REPLACE FUNCTION gtest.process_all() 
	RETURNS void AS $$
	
	BEGIN
		perform refit_all();
		perform resize_all();
		perform find_nearby(20);
		perform find_nearby(30);
		perform find_nearby(40);
		perform find_nearby(50);
		perform find_nearby(60);
		perform calc_benchmarks();
		update resized set sfc= (select avg(fitted.sfc) from fitted where pk=any(pks));
																								
	END;			
$$ LANGUAGE plpgsql;
																														
alter function process_all set search_path=gtest,public;																							
																								
																								
																								
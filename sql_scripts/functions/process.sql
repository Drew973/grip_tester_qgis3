SET SEARCH_PATH TO GTEST,PUBLIC;
																								
												
--updates resized where no data by looking for readings with sec_ch within tol.
CREATE OR REPLACE FUNCTION find_nearby(tol float=10) 
	RETURNS void AS $$
	
	BEGIN
	update gtest.resized set pks=array( select pk from gtest.fitted as f where f.sec=resized.sec and f.xsp=resized.xsp and f.reversed=resized.reversed and s_ch-tol<=sec_ch and sec_ch<=e_ch+tol) where empty_or_null(pks);
	--pks is {null} where no readings
	END;			
$$ LANGUAGE plpgsql;
																																

--updates resized for run where no data by looking for readings with sec_ch within tol.
CREATE OR REPLACE FUNCTION find_nearby(rn varchar,tol float=10) 
	RETURNS void AS $$
	declare
	sects varchar[]=array(select distinct sec from routes where run=rn);--sections in run

	BEGIN
	update gtest.resized set pks=array( select pk from gtest.fitted as f where f.sec=resized.sec and f.xsp=resized.xsp and f.reversed=resized.reversed and s_ch-tol<=sec_ch and sec_ch<=e_ch+tol) where run=rn and empty_or_null(pks);
	--pks is {null} where no readings
	END;			
$$ LANGUAGE plpgsql;



--updates resized for run where no data by looking for readings with sec_ch within tol.
CREATE OR REPLACE FUNCTION find_nearby(sects varchar[],tol float=10) 
	RETURNS void AS $$
	BEGIN
	update gtest.resized set pks=array( select pk from gtest.fitted as f where f.sec=resized.sec and f.xsp=resized.xsp and f.reversed=resized.reversed and s_ch-tol<=sec_ch and sec_ch<=e_ch+tol) 
	where sec=any(sects) and empty_or_null(pks);
	--pks is {null} where no readings
	END;			
$$ LANGUAGE plpgsql;
																								
--process all																								
CREATE OR REPLACE FUNCTION process() 
	RETURNS void AS $$
	
	BEGIN
		perform refit();
		perform resize();
		perform find_nearby(10);

		perform find_nearby(20);
		perform find_nearby(30);
		--perform find_nearby(40);
		--perform find_nearby(50);
		--perform find_nearby(60);
		--perform calc_benchmarks();
		perform update_sfc();
		update resized set sfc= (select avg(fitted.sfc) from fitted where pk=any(pks));--set sfc
																								
	END;			
$$ LANGUAGE plpgsql;
																														
alter function process() set search_path=gtest,public;	
																						
																								
																								
set search_path to gtest,public;

CREATE OR REPLACE FUNCTION process(rn varchar) 
	RETURNS void AS $$
	declare
		sects varchar[]=array(select distinct sec from routes where run=rn);--sections in run
		
	BEGIN
		perform refit(rn);
		perform resize(sects);
		perform find_nearby(sects,10);
		perform find_nearby(sects,20);
		perform find_nearby(sects,30);

		--if sects&&(array(select sec from network where gtest_benchmark)) then--any sec in benchmarks. &&=arrays have elements in common.
		--	perform calc_benchmarks();
		--end if	
		perform update_sfc(rn);
		
		update resized set sfc= (select avg(fitted.sfc) from fitted where pk=any(pks)) 
		where sec=any(sects);
		
	END;			
$$ LANGUAGE plpgsql;;
				
																				 
alter function process(varchar) set search_path=gtest,public;
																				 
																				 
--select process();
																				 
select process('test 52');
																				 
alter function process(varchar) set search_path=gtest,public;
																
																				 
--select process('test 51')																				 
select process()																				 
					
																				 
SET SEARCH_PATH TO GTEST,PUBLIC;

--resize everything.
CREATE OR REPLACE FUNCTION resize() 
	RETURNS void AS $$
	
	BEGIN
	
	delete from gtest.resized;

	insert into gtest.resized(sec,reversed,xsp,s_ch,e_ch,pks,geom)
	select pieces.sec,pieces.reversed,pieces.xsp,s_ch,e_ch,array_agg(pk) as pks,geom
	from gtest.pieces as pieces left join gtest.fitted as fitted on fitted.sec=pieces.sec and fitted.xsp=pieces.xsp and fitted.reversed=pieces.reversed and s_ch<=sec_ch and sec_ch<=e_ch
	group by pieces.sec,pieces.reversed,pieces.xsp,s_ch,e_ch,geom;
																		  
	END;			
$$ LANGUAGE plpgsql;


--redo resized run by deleting then reinserting all sections in run.
--delete then insert avoids problems if pieces/req changed.

CREATE OR REPLACE FUNCTION resize(rn varchar) 
	RETURNS void AS $$
	declare
		sects varchar[]=array(select distinct sec from routes where run=rn);--sections in run
	BEGIN
	--delete and reinsert any sections in run
	delete from resized where sec=any(sects);
	
	insert into resized
	select p.sec,p.reversed,p.xsp,s_ch,e_ch,array_agg(pk) as pks,avg(sfc) as sfc,geom
	from (select * from pieces where sec=any(sects)) as p left join fitted on fitted.sec=p.sec and fitted.xsp=p.xsp and fitted.reversed=p.reversed and s_ch<=sec_ch and sec_ch<=e_ch
	group by p.sec,p.reversed,p.xsp,s_ch,e_ch,geom;
								  
	END;			
$$ LANGUAGE plpgsql;
											 
alter function resize(varchar) set search_path=gtest,public;
											 

--redo resized run by deleting then reinserting all sections in run.
--delete then insert avoids problems if pieces/req changed.

CREATE OR REPLACE FUNCTION resize(sects varchar[]) 
	RETURNS void AS $$
	BEGIN
	--delete and reinsert any sections in run
	delete from resized where sec=any(sects);
	
	insert into resized
	select p.sec,p.reversed,p.xsp,s_ch,e_ch,array_agg(pk) as pks,avg(sfc) as sfc,geom
	from (select * from pieces where sec=any(sects)) as p left join fitted on fitted.sec=p.sec and fitted.xsp=p.xsp and fitted.reversed=p.reversed and s_ch<=sec_ch and sec_ch<=e_ch
	group by p.sec,p.reversed,p.xsp,s_ch,e_ch,geom;
								  
	END;			
$$ LANGUAGE plpgsql;
											 
alter function resize(varchar[]) set search_path=gtest,public;
											 
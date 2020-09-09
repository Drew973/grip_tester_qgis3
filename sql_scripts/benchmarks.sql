delete from benchmarks;

insert into benchmarks(sec,xsp,reversed,s_ch,e_ch,geom)
select sec,xsp,reversed,s_ch,e_ch,geom from pieces where (select benchmark from network where network.sec=pieces.sec);--benchmark section

update benchmarks set com=sec||'_'||xsp where s_ch=0;

--early																									 
--average gn where correct chainage and is benchmark and mid season
update benchmarks set early= (select avg(gn) from fitted where fitted.sec=benchmarks.sec and fitted.xsp=benchmarks.xsp and fitted.reversed=benchmarks.reversed and s_ch<=sec_ch and sec_ch<=e_ch and 
		  (select season from run_info where run_info.run=fitted.run)='early' and (select benchmark from run_info where run_info.run=fitted.run));

--10m either side where no value found
update benchmarks set early= (select avg(gn) from fitted where fitted.sec=benchmarks.sec and fitted.xsp=benchmarks.xsp and fitted.reversed=benchmarks.reversed and s_ch-10<=sec_ch and sec_ch<=e_ch+10 and 
		  (select season from run_info where run_info.run=fitted.run)='early' and (select benchmark from run_info where run_info.run=fitted.run))
	where early is null;
																				   
--mid																				   
--average gn where correct chainage and is benchmark and mid season
update benchmarks set mid= (select avg(gn) from fitted where fitted.sec=benchmarks.sec and fitted.xsp=benchmarks.xsp and fitted.reversed=benchmarks.reversed and s_ch<=sec_ch and sec_ch<=e_ch and 
		  (select season from run_info where run_info.run=fitted.run)='mid' and (select benchmark from run_info where run_info.run=fitted.run));

--10m either side where no value found
update benchmarks set mid= (select avg(gn) from fitted where fitted.sec=benchmarks.sec and fitted.xsp=benchmarks.xsp and fitted.reversed=benchmarks.reversed and s_ch-10<=sec_ch and sec_ch<=e_ch+10 and 
		  (select season from run_info where run_info.run=fitted.run)='mid' and (select benchmark from run_info where run_info.run=fitted.run))
	where mid is null;
																				 
																									 
--late																				   
--average gn where correct chainage and is benchmark and mid season
update benchmarks set late= (select avg(gn) from fitted where fitted.sec=benchmarks.sec and fitted.xsp=benchmarks.xsp and fitted.reversed=benchmarks.reversed and s_ch<=sec_ch and sec_ch<=e_ch and 
		  (select season from run_info where run_info.run=fitted.run)='late' and (select benchmark from run_info where run_info.run=fitted.run));

--10m either side where no value found
update benchmarks set late= (select avg(gn) from fitted where fitted.sec=benchmarks.sec and fitted.xsp=benchmarks.xsp and fitted.reversed=benchmarks.reversed and s_ch-10<=sec_ch and sec_ch<=e_ch+10 and 
		  (select season from run_info where run_info.run=fitted.run)='late' and (select benchmark from run_info where run_info.run=fitted.run))
	where late is null;
																				 
select * from benchmarks where early is null or mid is null order by sec,xsp,s_ch;	
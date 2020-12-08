drop view if exists benchmarks_view cascade;


create view benchmarks_view as
select sec,reversed,xsp,s_ch,e_ch,geom
,coalesce((select avg(gn) from fitted as f where (select season from gtest.run_info as ri where ri.run=f.run)='early' and f.sec=resized.sec and f.xsp=resized.xsp and f.reversed=resized.reversed and s_ch<=sec_ch and sec_ch<=e_ch)
	,(select avg(gn) from fitted as f where (select season from gtest.run_info as ri where ri.run=f.run)='early' and f.sec=resized.sec and f.xsp=resized.xsp and f.reversed=resized.reversed and s_ch-10<=sec_ch and sec_ch<=e_ch+10)) as early

,coalesce((select avg(gn) from fitted as f where (select season from gtest.run_info as ri where ri.run=f.run)='mid' and f.sec=resized.sec and f.xsp=resized.xsp and f.reversed=resized.reversed and s_ch<=sec_ch and sec_ch<=e_ch)
	,(select avg(gn) from fitted as f where (select season from gtest.run_info as ri where ri.run=f.run)='mid' and f.sec=resized.sec and f.xsp=resized.xsp and f.reversed=resized.reversed and s_ch-10<=sec_ch and sec_ch<=e_ch+10)) as mid
	  	  
,coalesce((select avg(gn) from fitted as f where (select season from gtest.run_info as ri where ri.run=f.run)='late' and f.sec=resized.sec and f.xsp=resized.xsp and f.reversed=resized.reversed and s_ch<=sec_ch and sec_ch<=e_ch)
	,(select avg(gn) from fitted as f where (select season from gtest.run_info as ri where ri.run=f.run)='late' and f.sec=resized.sec and f.xsp=resized.xsp and f.reversed=resized.reversed and s_ch-10<=sec_ch and sec_ch<=e_ch+10)) as late
	  
,case when s_ch=0 then sec||'_'||xsp else null end as com

from resized where (select gtest_benchmark from network where network.sec=resized.sec)
--order by sec,xsp,s_ch;




create or replace view benchmark_averages as
select avg(early) as early
,avg(mid) as mid
,avg(late) as late
,array_avg(array_agg(early)||array_agg(mid)||array_agg(late)) as total
from benchmarks_view;
		
													   
drop view if exists correction_factors;
													   
create or replace view correction_factors as													   
select total/early as early,total/mid as mid,total/late as late,0.89 as grip_to_sfc from benchmark_averages;
	
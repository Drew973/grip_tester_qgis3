
create or replace view gtest.correction_factors as
with av as (select array_mean(array(select early from benchmarks where not early is null)||array(select mid from benchmarks where not mid is null)||array(select late from benchmarks where not late is null)) as val)
	select  avg(early) as av_early,
	(select val from av)/avg(early) as early,
	(select val from av)/avg(mid) as mid,
	avg(mid) as av_mid,
	(select val from av)/avg(late) as late,
	avg(late) as av_late,
	0.89 as grip_to_sfc							  
	from gtest.benchmarks;	
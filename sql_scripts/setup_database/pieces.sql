
--requested sections into 10m pieces.
--when reversed s_ch and e_ch are 'wrong' way around.

drop view if exists pieces cascade;

create view pieces as

with p as(
select requested.sec,reversed,xsp,meas_len,generate_series(0,cast(meas_len as numeric),10) as s_ch
from requested inner join network on requested.sec=network.sec)

,f as (select *,coalesce(lead(s_ch) over(partition by sec,xsp order by s_ch),meas_len) as e_ch from p order by sec,s_ch)

select sec,reversed,xsp,cast(s_ch as float),e_ch,
case when reversed then get_line(sec,e_ch,cast(s_ch as float)) when not reversed then get_line(sec,cast(s_ch as float),e_ch) end
as geom										   
	from f where s_ch!=e_ch;
											   
											   
select *,st_asText(geom) from pieces --where lower(st_asText(geom)) like '%point%'		

--requested sections into 10m pieces.
--when reversed s_ch and e_ch are 'wrong' way around.

create or replace view gtest.pieces as

with p as(
select r.sec,reversed,xsp,meas_len,generate_series(0,cast(meas_len as numeric),10) as s_ch
from gtest.requested as r inner join network on r.sec=network.sec)

,f as (select *,coalesce(lead(s_ch) over(partition by sec,xsp order by s_ch),meas_len) as e_ch from p order by sec,s_ch)

select sec,reversed,xsp,cast(s_ch as float),e_ch,
case when reversed then get_line(sec,e_ch,cast(s_ch as float)) when not reversed then get_line(sec,cast(s_ch as float),e_ch) end
as geom										   
	from f where s_ch!=e_ch;			   

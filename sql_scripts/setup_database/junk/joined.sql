drop view if exists joined cascade;

create view joined as select 
s10.ref,
s10.ch,
left_skid,
speed,
air_temp,
surface_temp,
pt,
st_makeline(pt,lead(pt) over (partition by zm3.ref order by zm3.ch) ) as vect 
from s10 left join zm3 on zm3.ref=s10.ref and zm3.ch=s10.ch;
;

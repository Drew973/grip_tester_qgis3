drop table if exists fitted2;
--select sec,reversed,xsp,s_ch,e_ch,geom,array(select gn from fitted where fitted.sec=pieces.sec and fitted.xsp=pieces.xsp and s_ch<=sec_ch and sec_ch<=e_ch and s_ch<e_ch) from pieces

create table fitted2 as
select pieces.sec,pieces.reversed,pieces.xsp,s_ch,e_ch,array_agg(pk) as pks,avg(sfc) as sfc,geom
from pieces left join fitted on fitted.sec=pieces.sec and fitted.xsp=pieces.xsp and fitted.reversed=pieces.reversed and s_ch<=sec_ch and sec_ch<=e_ch
group by pieces.sec,pieces.reversed,pieces.xsp,s_ch,e_ch,geom;

create index on fitted2 using gist(geom);
--update fitted2 set gn=avg(unnest(gns));
						
update fitted2 set (pks,sfc)=
(select array_agg(pk),avg(sfc) from fitted 
where fitted.sec=fitted2.sec and fitted.xsp=fitted2.xsp and fitted.reversed=fitted2.reversed and s_ch-10<=sec_ch and sec_ch<=e_ch+10
)
where sfc is null;
						
						
select * from fitted2;
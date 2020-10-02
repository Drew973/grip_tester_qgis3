drop table if exists fitted2;
create table fitted2 as
select pieces.sec,pieces.xsp,s_ch,e_ch,geom,ref,ch,sc,speed,air_temp,surface_temp,pt,sec_ch,survey_date
from pieces left join fitted on fitted.sec=pieces.sec and fitted.xsp=pieces.xsp and s_ch<=sec_ch and sec_ch<=e_ch and s_ch<e_ch;
--13s
create index on fitted2(sec,xsp);
create index on fitted2(sec,xsp);


update fitted2 set (ref,ch,sc,speed,air_temp,surface_temp,pt,sec_ch,survey_date)=
(select ref,ch,sc,speed,air_temp,surface_temp,pt,sec_ch,survey_date
from fitted 
where fitted.sec=fitted2.sec and fitted.xsp=fitted2.xsp and s_ch-10<=sec_ch and sec_ch<=e_ch+10
order by left_skid
limit 1)
where sc is null;	
--13s



create index on fitted2(sec);
create index on fitted2(xsp);
create index on fitted2(reversed);
create index on fitted2(s_ch);
create index on fitted2(e_ch);
create index on fitted2 using gist(geom);




drop table if exists sedates;
create table sedates as select sec,xsp,min(survey_date) as sdate,max(survey_date) as edate from fitted2 group by sec,xsp;																										  
alter table sedates add primary key(sec,xsp);
--<1s
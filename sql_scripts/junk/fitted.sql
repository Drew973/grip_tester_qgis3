drop table if exists fitted cascade;

create table fitted as
select routes.run,ch,reversed,left_skid,left_skid_to_sc(100*left_skid,speed) as sc,f_line,speed,air_temp,surface_temp,pt,vect,sec,xsp,meas_sec_ch(sec,pt) as sec_ch
from r inner join routes on routes.run=r.run and s<=f_line and f_line<=e;

create index on fitted(run);
create index on fitted(sec);
create index on fitted(xsp);
create index on fitted(sec_ch);		
delete from fitted;

insert into fitted(run,ch,reversed,gn,f_line,speed,pt,vect,sec,xsp,sec_ch)

select routes.run,ch,reversed,left_skid as gn,f_line,speed,pt,vect,sec,xsp,
case when start_sec_ch is null or end_sec_ch is null or start_sec_ch<0 or end_sec_ch<0 then meas_sec_ch(sec,pt) 
else ch_to_sec_ch(ch,(select ch from r as res where r.run=res.run and f_line=s),(select ch from r as res where r.run=res.run and f_line=e),start_sec_ch,end_sec_ch)
end

as sec_ch

from r inner join routes on routes.run=r.run and s<=f_line and f_line<=e;

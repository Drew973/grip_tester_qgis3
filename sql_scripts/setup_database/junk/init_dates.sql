insert into dates
select distinct ref,cast(null as date) from joined;



update dates set survey_date=to_date('2019-10-02','yy-mm-dd');
update dates set survey_date=to_date('2019-10-03','yy-mm-dd') where ref in('Sx3010','Sx3011','Sx3012','Sx3013','Sx3014','Sx3015');

update dates set survey_date=to_date('2019-10-04','yy-mm-dd') where ref in('Sx3016');
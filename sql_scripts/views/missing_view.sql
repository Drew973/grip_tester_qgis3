--if one distinct note in requested where sec=sect then return this. otherwise return something like
--'{CL1,CL2}:Cl1 and CL2 share this note;CR1:note for CR1'
CREATE OR REPLACE FUNCTION gtest.make_comment(sect varchar) 
	RETURNS varchar AS $$
	DECLARE
		r record;					
		res varchar='';
		n_notes int=cardinality(array(select distinct(note) from gtest.requested where sec=sect and cardinality(hmds)=0));
	
	BEGIN
		if n_notes=1 then
			return distinct(note) from gtest.requested where sec=sect and cardinality(hmds)=0;
		end if;
								   
								   
		for r in (select note,array_agg(xsp)::varchar as xsps from gtest.requested where sec=sect and cardinality(hmds)=0 group by note) loop
			if res='' then
				res=res||r.xsps||':'||r.note;
			else
				res=res||';'||r.xsps||':'||r.note;
			end if;
								   
		end loop;											

										
	return res;
	END;			
$$ LANGUAGE plpgsql;
										

--drop view if exists gtest.missing_view cascade;
--create view gtest.missing_view as select road_class(sec) as road_class,sec as section,right(left(array_agg(xsp)::varchar,-1),-1) as direction,gtest.make_comment(sec) as Comment from gtest.requested where cardinality(hmds)=0 group by sec;			   
--view for making submission sheet




drop view if exists missing_view;
create view missing_view as

drop view if exists missing_view;
create view missing_view as

select road_class
,sec as section,
array_to_string(xsps,',') as direction
,case when cardinality(notes)=1 then notes[1]
	else long_com
	end as comment
																									   
from (select road_class(sec) as road_class
	  ,sec
	  ,array_agg(xsp) as xsps
	  ,ARRAY_TO_STRING(array_agg(xsp||':'||note),'. ') as long_com
	  ,array_distinct(array_agg(note)) as notes
	  from requested where cardinality(hmds)=0 group by sec) a;			   


--if one distinct note in requested where sec=sect then return this. otherwise return something like
--'{CL1,CL2}:Cl1 and CL2 share this note;CR1:note for CR1'
CREATE OR REPLACE FUNCTION make_comment(sect varchar) 
	RETURNS varchar AS $$
	DECLARE
		r record;					
		res varchar='';
		n_notes int=cardinality(array(select distinct(note) from requested where sec=sect and cardinality(hmds)=0));
	
	BEGIN
		if n_notes=1 then
			return distinct(note) from requested where sec=sect and cardinality(hmds)=0;
		end if;
								   
								   
		for r in (select note,array_agg(xsp)::varchar as xsps from requested where sec=sect and cardinality(hmds)=0 group by note) loop
			if res='' then
				res=res||r.xsps||':'||r.note;
			else
				res=res||';'||r.xsps||':'||r.note;
			end if;
								   
		end loop;											

										
	return res;
	END;			
$$ LANGUAGE plpgsql;
										

drop view if exists missing_view cascade;
create view missing_view as select road_class(sec) as road_class,sec as section,right(left(array_agg(xsp)::varchar,-1),-1) as direction,make_comment(sec) as Comment from requested where cardinality(hmds)=0 group by sec;			   
--view for making submission sheet



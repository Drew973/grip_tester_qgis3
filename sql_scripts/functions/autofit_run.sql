CREATE OR REPLACE FUNCTION autofit_run(rn varchar) 
	RETURNS void AS $$
	
	BEGIN

		update readings set ps=ps(pt,vect,0.833,1,1,0) where run=rn;
		update readings set ps_text=cast(ps as varchar[]) where run=rn;

		delete from routes where run=rn and note='auto';						  									   
											   
		with a as (select ps[1] as p,unnest(array_cluster_int(array_agg(f_line),5)) from readings where run=rn group by run,ps[1])
			,b as (select (p).sec as sec,(p).rev as rev,lower(unnest) as s,upper(unnest) as e from a)																											   
																													   
		insert into routes(run,sec,reversed,s,e,note) 										  
		select rn,sec,rev,s,e,'auto' from b
		where not sec is null
		and 0=(select count(sec) from routes as r where r.run=rn and abs(r.s-b.s)<5 and abs(r.e-b.e)<5)--no existing entry with start and end within 50m
;

	END;			
$$ LANGUAGE plpgsql;
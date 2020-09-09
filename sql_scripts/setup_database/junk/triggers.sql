CREATE OR REPLACE FUNCTION routes_change() RETURNS TRIGGER AS $routes$
   BEGIN
	  delete from fitted where ref=new.ref and sec=new.sec and xsp=new.xsp;
	  --perform insert_into_fitted(ref,sec,xsp,s_ch,e_ch) from routes where ref=new.ref and sec=new.sec and xsp=new.xsp;
	  insert into fitted select *,new.sec,new.xsp,meas_sec_ch(new.sec,pt) from joined where ref=new.ref and new.s_ch<=ch and ch<=new.e_ch;
	  perform fitted2_redo_sec(new.sec,new.xsp);
	  RETURN NEW;
   END;
$routes$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION routes_delete() RETURNS TRIGGER AS $routes$
   BEGIN
	  delete from fitted where ref=old.ref and sec=old.sec and xsp=old.xsp;
--insert into fitted select 
	  perform fitted2_redo_sec(old.sec,old.xsp);
	  RETURN NEW;
   END;
$routes$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION fitted2_redo_sec(sect varchar,x varchar) 
RETURNS void AS $$
	BEGIN
		--update fitted2 set (ref,ch,left_skid,speed,air_temp,surface_temp,pt,sec_ch)=select(null,null,null,null,null,null,null,null) where sec=sect and xsp=x;

		if x='CL1' then
			update fitted2 set (ref,ch,left_skid,speed,air_temp,surface_temp,pt,sec_ch)=
			(select ref,ch,left_skid,speed,air_temp,surface_temp,pt,sec_ch 
			from fitted 
			where fitted.sec=sect and fitted.xsp='CL1' and s_ch<=sec_ch and sec_ch<=e_ch
			order by left_skid
			limit 1)
			where sec=sect and xsp=x;
			
			
			--lowest left_skid from nearby
			update fitted2 set (ref,ch,left_skid,speed,air_temp,surface_temp,pt,sec_ch)=
			(select ref,ch,left_skid,speed,air_temp,surface_temp,pt,sec_ch 
			from fitted 
			where fitted.sec=sect and fitted.xsp='CL1' and s_ch-10<=sec_ch and sec_ch<=e_ch+10
			order by left_skid
			limit 1)
			where sec=sect and xsp=x and left_skid is null;	
		
		end if;
			
		if x='CR1' then
			update fitted2 set (ref,ch,left_skid,speed,air_temp,surface_temp,pt,sec_ch)=
			(select ref,ch,left_skid,speed,air_temp,surface_temp,pt,sec_ch 
			from fitted 
			where fitted.sec=sect and fitted.xsp='CR1' and e_ch<=sec_ch and sec_ch<=s_ch
			order by left_skid
			limit 1	)
			where sec=sect and xsp=x;

			
			--nearby
			update fitted2 set (ref,ch,left_skid,speed,air_temp,surface_temp,pt,sec_ch)=
			(select ref,ch,left_skid,speed,air_temp,surface_temp,pt,sec_ch 
			from fitted 
			where fitted.sec=sect and fitted.xsp='CR1' and e_ch-10<=sec_ch and sec_ch<=s_ch+10
			order by left_skid
			limit 1	)
			where sec=sect and xsp=x and left_skid is null;

		end if;		
		
	END;			
$$ LANGUAGE plpgsql;


drop trigger if exists routes_insert on routes;

CREATE TRIGGER routes_insert
  after insert
  ON routes
  FOR EACH ROW
  EXECUTE PROCEDURE routes_change();
  
drop trigger if exists routes_update on routes;

CREATE TRIGGER routes_update
  after update
  ON routes
  FOR EACH ROW
  EXECUTE PROCEDURE routes_change();

drop trigger if exists routes_delete on routes;

CREATE TRIGGER routes_delete
  after delete
  ON routes
  FOR EACH ROW
  EXECUTE PROCEDURE routes_delete();
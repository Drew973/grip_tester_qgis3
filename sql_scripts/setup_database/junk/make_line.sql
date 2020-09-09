CREATE OR REPLACE FUNCTION make_line(sect varchar,s_meas float,e_meas float,rev bool) 
RETURNS geometry('Linestring') AS $$
		declare
			len float =meas_len from network where sec=sect;
			f1 float=s_meas/len;
			f2 float=e_meas/len;
			L geometry=geom from network where sec=sect;
			
        BEGIN	
				if rev then
					f1=1-f1;
					f2=1-f2;
				end if;
		
				if f1<0 then
					f1=0;
				end if;
				
				if f1>1 then
					f1=1;
				end if; 

				if f2>1 then
					f2=1;
				end if; 

				if f2<0 then
					f2=0;
				end if; 
				
				if f1=f2 then
					return null;
				end if;				
				
				if f2>f1 then
					return ST_LineSubstring(L,f1,f2);
				else
					return st_reverse(ST_LineSubstring(L,f2,f1));
				end if;
													   
		END;			
$$ LANGUAGE plpgsql;
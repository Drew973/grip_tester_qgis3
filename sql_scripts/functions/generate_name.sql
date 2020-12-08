--adds _ and number to end of name to make unique run
CREATE OR REPLACE FUNCTION generate_name(preferable varchar) 
RETURNS varchar AS $$			  		
	Declare n varchar=preferable;
			i int=1;			
	BEGIN
	
		while (select count(run) from run_info where run=n)>0 loop
			n=preferable||'_'||i::varchar;
			i=i+1;
		end loop;
		
		return n;
	END;			
$$ LANGUAGE plpgsql;
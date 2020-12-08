CREATE OR REPLACE FUNCTION interpolate(x float,x1 float,y1 float,x2 float,y2 float) 
RETURNS float AS $$
		declare 	
			m float=(y2-y1)/(x2-x1);
			c float=y1-m*x1;
									  
        BEGIN	
			return m*x+c;
		END;			
$$ LANGUAGE plpgsql;
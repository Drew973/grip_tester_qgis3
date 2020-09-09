CREATE OR REPLACE FUNCTION coverage(sect varchar,r bool,x varchar) 
RETURNS float AS $$
Declare
	should_be int=count(sec) from fitted2 where sec=sect and reversed=r and xsp=x;
	have int=count(sec) from fitted2 where sec=sect and reversed=r and xsp=x and not gn is null;
	BEGIN
		if r and one_way from network where sec=sect then
			return Null;
		end if;
			
		if should_be=0 then
			return null;
		end if;
		
		return  100*have/should_be;
		
	END;			
$$ LANGUAGE plpgsql;
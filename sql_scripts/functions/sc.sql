CREATE OR REPLACE FUNCTION left_skid_to_sc(ls int,speed int) 
RETURNS float AS $$

	BEGIN
	if speed<25 or speed>85 then
		return Null;
	end if;

	return 0.78*0.01*0.001*ls*(799+4.77*ls-0.0152*ls*ls);
	END;			
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION left_skid_to_sc(ls float,speed float) 
RETURNS float AS $$

	BEGIN
	if speed<25 or speed>85 then
		return Null;
	end if;

	return 0.78*0.01*0.001*ls*(799+4.77*ls-0.0152*ls*ls);
	END;			
$$ LANGUAGE plpgsql;
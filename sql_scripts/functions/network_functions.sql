CREATE OR REPLACE FUNCTION meas_len(sect varchar) RETURNS float AS
'SELECT cast(meas_len as float) from gtest.network where sec=sect' LANGUAGE sql IMMUTABLE;

CREATE OR REPLACE FUNCTION road(sect varchar) RETURNS varchar AS
'SELECT road from gtest.network where sec=sect' LANGUAGE sql IMMUTABLE;

CREATE OR REPLACE FUNCTION is_rbt(sect varchar) RETURNS bool AS
'SELECT rbt from gtest.network where sec=sect' LANGUAGE sql IMMUTABLE;

CREATE OR REPLACE FUNCTION near_rbt(pt geometry('point'),dist float=5) RETURNS bool AS
'SELECT 0<count(sec) from gtest.network  where rbt and st_dwithin(pt,geom,dist)' LANGUAGE sql IMMUTABLE;

CREATE OR REPLACE FUNCTION invert_ch(ch float,sect varchar) RETURNS float AS
'SELECT meas_len-ch from gtest.network  where sec=sect' LANGUAGE sql IMMUTABLE;
					   

CREATE OR REPLACE FUNCTION ch_to_point(sect varchar,chainage float) 
RETURNS geometry('point') AS $$
		declare 	
			L float=meas_len from gtest.network  where sec=sect;
			f float=chainage/L;			
			geom geometry('linestring')=geom from gtest.network  where sec=sect;
        BEGIN	
			if f>1  then 
				f=1;
			end if;
			
			if f<0 then
				f=0;
			end if;
			
			return ST_LineInterpolatePoint(geom,f);
		END;			
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION meas_sec_ch(sect varchar,pt geometry('point'),rev bool=False) 
RETURNS float AS $$
	declare 
		geom geometry=geom from gtest.network  where sec=sect;
		ml float=meas_len from gtest.network  where sec=sect;
	BEGIN
		if rev then
			return ml*(1-st_linelocatepoint(geom,pt));
		 else
		 	return ml*st_linelocatepoint(geom,pt);
		end if;
	END;			
$$ LANGUAGE plpgsql;										
																
CREATE OR REPLACE FUNCTION  floor_meas_len(sect varchar) 
RETURNS int AS $$
	declare f int=10*floor(meas_len/10) from gtest.network  where sec=sect;
        BEGIN	
			if f<meas_len from gtest.network  where sec=sect then
				return f;
			else 
				return f-10;
			end if;
		END;			
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION invert_ch(ch float,sect varchar) 
RETURNS float AS $$
        BEGIN	
			return meas_len-ch from gtest.network  where sec=sect;
		END;			
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION int_meas_len(sect varchar) 
RETURNS int AS $$
        BEGIN	
			return meas_len from gtest.network  where sec=sect;
		END;			
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION calc_to_meas(calc float,sect varchar) 
RETURNS float AS $$
        BEGIN	
			return calc*(select meas_len from gtest.network  where sec=sect)/(select calc_len from gtest.network  where sec=sect);
		END;			
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION calc_to_meas(calc int,sect varchar) 
RETURNS float AS $$
        BEGIN	
			return calc*(select meas_len from gtest.network  where sec=sect)/(select calc_len from gtest.network  where sec=sect);
		END;			
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION road_class(sect varchar) 
RETURNS varchar AS $$
	declare
		c varchar=upper(left(sect,1));
    BEGIN	
		if c='A' or c='B'or c='C' then
			return c;
		else
			return 'U';
		end if;
		END;			
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION xsp_reversed(x varchar) 
RETURNS bool AS $$
        BEGIN	
			return x like('CR');
		END;			
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION has_info(s varchar)
RETURNS Bool AS $$											 
    BEGIN
		if s is null then
			return false;
		end if;
		
		if s='' then
			return false;
		end if;
	
	return True;
	END;			
$$ LANGUAGE plpgsql;


--part of linestring  from start_ch to end_ch. len=noninal length. chainages in terms of nominal length

CREATE OR REPLACE FUNCTION make_line(L geometry('linestring'),len float,start_ch float,end_ch float) 
RETURNS geometry('linestring') AS $$
		declare
			f1 float;
			f2 float;
        BEGIN	
				f1=start_ch/len;
				f2=end_ch/len;
				
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
				
				if f2>f1 then
					return ST_LineSubstring(L,f1,f2);
				else
					return st_reverse(ST_LineSubstring(L,f2,f1));
				end if;
													   
		END;			
$$ LANGUAGE plpgsql;
													   

--returns linestring from start_ch to end_ch of section, start_ch and end_ch in terms of meas_len.
													   					
CREATE OR REPLACE FUNCTION get_line(sect varchar,start_ch float,end_ch float) 
RETURNS geometry AS $$
		declare g geometry=geom from gtest.network  where sec=sect;
        BEGIN	
				return make_line(g,meas_len(sect),start_ch,end_ch);
		END;			
$$ LANGUAGE plpgsql;	
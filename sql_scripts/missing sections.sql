drop table if exists missing_sections;

create table missing_sections as
select sec,reversed,xsp,note, 
case 
when not reversed then (select geom from network where network.sec=requested.sec) 
when reversed then (select st_reverse(geom) from network where network.sec=requested.sec) 
end
as geom
from requested where cardinality(hmds)=0;

create index on missing_sections using gist(geom);	
    drop table if exists s10 cascade;

    create table s10
    (
    ch float,
    speed int,
    something int,
    left_skid int,
    right_skid int,
    air_temp int,
    surface_temp int,
    ref varchar references run_info(run) ON DELETE CASCADE,
	primary key(ref,ch)
    );
	

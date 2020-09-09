   drop table if exists zm3 cascade;

    create table zm3
    (
    ch float,
    z float,
	pt geometry('point',27700),
    a int,
    b float,
    ref varchar references run_info(run) ON DELETE CASCADE,
	primary key(ref,ch)
    );
	
create index on zm3 using gist(pt);


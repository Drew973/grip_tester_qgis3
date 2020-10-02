drop type if exists sec_rev cascade;

CREATE TYPE sec_rev AS
   (
     sec VARCHAR,
     rev bool
   );

drop type if exists test_season cascade;
CREATE TYPE test_season AS ENUM ('early', 'mid', 'late','');
alter table margin change margin margin decimal(16,2) not null default '0';
alter table margin change withdraw withdraw decimal(16,2) not null default '0';
alter table margin change freeze freeze decimal(16,2) not null default '0';

alter table contract change amount amount decimal(16,2) not null default '0';
alter table contract change total_amount total_amount decimal(16,2) not null default '0';

alter table milestone change amount amount decimal(16,2) not null default '0';

alter table margin_record change amount amount decimal(16,2) not null default '0';
alter table margin_record change currently currently decimal(16,2) not null default '0';
alter table margin_record change margin margin decimal(16,2) not null default '0';

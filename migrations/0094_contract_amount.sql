alter table contract change amount amount decimal(12,2) not null default 0;

alter table contract change total_amount total_amount decimal(12,2) not null default 0;

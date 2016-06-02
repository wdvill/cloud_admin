alter table milestone add actual_amount decimal(8,2) not null default '0';

alter table contract add finish_by varchar(20) not null default "";

alter table milestone_record drop rtype;

alter table milestone_record add reason varchar(500) not null default "";

alter table milestone_record add audit_attachment_id int not null default 0;

drop table weekstone_record;

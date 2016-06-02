alter table team add uuid varchar(36) not null default "";

alter table team add index(uuid);

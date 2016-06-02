alter table user add uuid varchar(36) not null default "";

alter table user add index(uuid);

alter table job drop job_uuid;

alter table job add job_uuid varchar(36) not null default "";

alter table job add index(job_uuid);

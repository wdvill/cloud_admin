alter table job drop job_type;

alter table job drop job_desc;

alter table job change platforms platforms varchar(100) not null default "";

alter table job change integrated_api integrated_api varchar(100) not null default "";

alter table job drop skills_other;

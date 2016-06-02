alter table profile change is_notice is_notice tinyint(1) not null default 0;

alter table team change name name varchar(150) not null default "";

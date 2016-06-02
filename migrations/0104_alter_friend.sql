alter table friend drop friend_id;

alter table friend add ftype varchar(10) not null default "";

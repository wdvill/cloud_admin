alter table shotrecord add user_id int not null default 0;

alter table shotrecord add team_id int not null default 0;

alter table shotrecord add index(user_id);

alter table shotrecord add index(team_id);

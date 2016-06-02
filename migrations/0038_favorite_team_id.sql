alter table favorite add team_id int not null default 0;

alter table favorite add index(team_id);

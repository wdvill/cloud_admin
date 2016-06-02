alter table margin_record drop bankcard;

alter table margin_record add team_id int not null default 0;

alter table margin_record add index(team_id);

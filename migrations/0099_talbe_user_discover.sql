CREATE TABLE `user_discover` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL DEFAULT '0',
  `discover_num` int(11) NOT NULL DEFAULT '0',
  `view_num` int(11) NOT NULL DEFAULT '0',
  `period` int(11) NOT NULL DEFAULT '0',
  `update_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

alter table user_statistics add update_at datetime default null;

alter table user_statistics add year_amount decimal(10,2) not null default 0;

alter table user_statistics add season_invite int not null default 0;

alter table user_statistics add season_reply int not null default 0;

alter table user_statistics add season_day_reply int not null default 0;

alter table user_statistics add season_proposal int not null default 0;

alter table user_statistics add season_view int not null default 0;

alter table user_statistics add season_interview int not null default 0;

alter table user_statistics add season_hire int not null default 0;

alter table proposal add day_reply tinyint(1) not null default 0;

CREATE TABLE `notify_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mtype` varchar(30) NOT NULL DEFAULT '',
  `name` varchar(100) NOT NULL DEFAULT '',
  `ename` varchar(200) NOT NULL DEFAULT '',
  `who` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `who` (`who`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `notify_setting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL DEFAULT '0',
  `team_id` int(11) NOT NULL DEFAULT '0',
  `mtype` varchar(30) NOT NULL DEFAULT '',
  `is_send` tinyint(1) NOT NULL DEFAULT '0',
  `create_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `team_id` (`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
alter table profile add recomm_rate varchar(20) not null default "";
alter table profile add last_recomm datetime default null;

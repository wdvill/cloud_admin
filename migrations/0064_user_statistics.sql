alter table profile add coop_rate int not null default 0;

alter table team_statistics add aver_score double not null default 0;

alter table team_statistics change total_amount total_amount decimal(10,2) not null default 0;

alter table team_statistics drop create_at;


CREATE TABLE `user_statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL DEFAULT '0',
  `eveluate_num` int(11) NOT NULL DEFAULT '0',
  `score` int(11) NOT NULL DEFAULT '0',
  `aver_score` double NOT NULL DEFAULT '0',
  `total_amount` decimal(10,2) NOT NULL DEFAULT '0.00',
  `hours` int(11) NOT NULL DEFAULT '0',
  `proposal` int(11) NOT NULL DEFAULT '0',
  `success` int(11) NOT NULL DEFAULT '0',
  `recommend` int(11) NOT NULL DEFAULT '0',
  `coop` int(11) NOT NULL DEFAULT '0',
  `coop_success` int(11) NOT NULL DEFAULT '0',
  `coop_two` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

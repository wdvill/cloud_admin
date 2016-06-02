CREATE TABLE `notify` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL DEFAULT '0',
  `team_id` int(11) NOT NULL DEFAULT '0',
  `mtype` varchar(50) NOT NULL DEFAULT '',
  `read_at` datetime DEFAULT NULL,
  `create_at` datetime NOT NULL,
  `extra` varchar(1000) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `team_id` (`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `team_statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL DEFAULT '0',
  `team_id` int(11) NOT NULL DEFAULT '0',
  `eveluate_num` int(11) NOT NULL DEFAULT '0',
  `total_amount` decimal(9,2) NOT NULL DEFAULT '0.00',
  `score` int(11) NOT NULL DEFAULT '0',
  `hours` int(11) NOT NULL DEFAULT '0',
  `jobs` int(11) NOT NULL DEFAULT '0',
  `hires` int(11) NOT NULL DEFAULT '0',
  `open_jobs` int(11) NOT NULL DEFAULT '0',
  `create_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `team_id` (`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

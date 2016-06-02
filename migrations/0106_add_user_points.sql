CREATE TABLE `user_points` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL DEFAULT '0',
  `category` tinyint(1) NOT NULL DEFAULT '0',
  `avatar` tinyint(1) NOT NULL DEFAULT '0',
  `title` tinyint(1) NOT NULL DEFAULT '0',
  `overview` tinyint(1) NOT NULL DEFAULT '0',
  `email` tinyint(1) NOT NULL DEFAULT '0',
  `skills` tinyint(1) NOT NULL DEFAULT '0',
  `english` tinyint(1) NOT NULL DEFAULT '0',
  `other_language` tinyint(1) NOT NULL DEFAULT '0',
  `workload` tinyint(1) NOT NULL DEFAULT '0',
  `hourly` tinyint(1) NOT NULL DEFAULT '0',
  `level` tinyint(1) NOT NULL DEFAULT '0',
  `employment` tinyint(1) NOT NULL DEFAULT '0',
  `education` tinyint(1) NOT NULL DEFAULT '0',
  `portfolio` tinyint(1) NOT NULL DEFAULT '0',
  `location` tinyint(1) NOT NULL DEFAULT '0',
  `address` tinyint(1) NOT NULL DEFAULT '0',
  `postcode` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



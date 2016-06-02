CREATE TABLE `job` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL DEFAULT '0',
  `team_id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(100) NOT NULL DEFAULT '',
  `category_id` int(11) NOT NULL DEFAULT '0',
  `skills` varchar(1000) NOT NULL DEFAULT '',
  `duration` int(11) NOT NULL DEFAULT '0',
  `workload` int(11) NOT NULL DEFAULT '0',
  `level` varchar(10) NOT NULL DEFAULT '',
  `hires` int(11) NOT NULL DEFAULT '0',
  `attachment_id` int(11) NOT NULL DEFAULT '0',
  `job_type` varchar(20) NOT NULL DEFAULT '',
  `description` longtext,
  `stage` varchar(20) NOT NULL DEFAULT '',
  `budget` decimal(10,2) NOT NULL DEFAULT '0.00',
  `paymethod` varchar(10) NOT NULL DEFAULT '',
  `status` varchar(10) NOT NULL DEFAULT '',
  `create_at` datetime NOT NULL,
  `update_at` datetime NOT NULL,
  `platforms` varchar(50) NOT NULL DEFAULT '',
  `integrated_api` tinyint(1) NOT NULL DEFAULT '0',
  `languages` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `team_id` (`team_id`),
  KEY `category_id` (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL DEFAULT '',
  `description` varchar(500) NOT NULL DEFAULT '',
  `parent_id` int(11) NOT NULL DEFAULT '0',
  `create_at` datetime NOT NULL,
  `level` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `parent` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `attachment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL DEFAULT '',
  `size` int(11) NOT NULL DEFAULT '0',
  `md5` char(32) NOT NULL DEFAULT '',
  `path` varchar(250) NOT NULL DEFAULT '',
  `create_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

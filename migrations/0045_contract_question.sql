alter table question add qtype varchar(20) not null default "";

CREATE TABLE `contract` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL DEFAULT '0',
  `job_id` int(11) NOT NULL DEFAULT '0',
  `team_id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(30) NOT NULL DEFAULT '',
  `invoice` varchar(30) NOT NULL DEFAULT '',
  `amount` decimal(8,2) NOT NULL DEFAULT '0.00',
  `hourly` decimal(8,2) NOT NULL DEFAULT '0.00',
  `workload` int(11) NOT NULL DEFAULT '0',
  `status` varchar(20) NOT NULL DEFAULT '',
  `total_amount` decimal(8,2) NOT NULL DEFAULT '0.00',
  `bonus` decimal(6,2) NOT NULL DEFAULT '0.00',
  `attachment_id` int(11) NOT NULL DEFAULT '0',
  `message` varchar(500) NOT NULL DEFAULT '',
  `question_id` int(11) NOT NULL DEFAULT '0',
  `reason` varchar(500) NOT NULL DEFAULT '',
  `start_at` datetime DEFAULT NULL,
  `end_at` datetime DEFAULT NULL,
  `accept_at` datetime DEFAULT NULL,
  `create_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `job_id` (`job_id`),
  KEY `user_id` (`user_id`),
  KEY `team_id` (`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `milestone` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contract_id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(20) NOT NULL DEFAULT '',
  `amount` decimal(8,2) NOT NULL DEFAULT '0.00',
  `actual_amount` decimal(8,2) NOT NULL DEFAULT '0.00',
  `status` varchar(20) NOT NULL DEFAULT '',
  `end_at` datetime NOT NULL,
  `create_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `contract_id` (`contract_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `milestone_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `milestone_id` int(11) NOT NULL DEFAULT '0',
  `attachment_id` int(11) NOT NULL DEFAULT '0',
  `amount` decimal(8,2) NOT NULL DEFAULT '0.00',
  `message` varchar(500) NOT NULL DEFAULT '',
  `rtype` varchar(20) NOT NULL DEFAULT '',
  `create_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `milestone_id` (`milestone_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `contract_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contract_id` int(11) NOT NULL DEFAULT '0',
  `rtype` varchar(20) NOT NULL DEFAULT '',
  `extra` longtext,
  `create_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `contract_id` (`contract_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

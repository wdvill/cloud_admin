CREATE TABLE `help_topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL DEFAULT '',
  `ename` varchar(100) NOT NULL DEFAULT '',
  `create_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `help_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic_id` int(11) NOT NULL DEFAULT '0',
  `uuid` varchar(32) NOT NULL DEFAULT '',
  `title` varchar(100) NOT NULL DEFAULT '',
  `etitle` varchar(100) NOT NULL DEFAULT '',
  `answer` text NOT NULL,
  `eanswer` text NOT NULL,
  `hotspot` tinyint(1) NOT NULL DEFAULT '0',
  `sortord` int(11) NOT NULL DEFAULT '0',
  `create_at` datetime NOT NULL,
  `update_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `topic_id` (`topic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

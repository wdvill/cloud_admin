CREATE TABLE `session` (
  `session_key` varchar(40) NOT NULL DEFAULT '',
  `expire_at` datetime NOT NULL,
  `user_id` int(11) NOT NULL DEFAULT '0',
  KEY `session_key` (`session_key`),
  KEY `expire_at` (`expire_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `address` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL DEFAULT '',
  `level` int(11) NOT NULL DEFAULT '0',
  `parent` int(11) NOT NULL DEFAULT '0',
  `code` varchar(10) NOT NULL DEFAULT '',
  `create_at` datetime NOT NULL,
  `ename` varchar(150) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

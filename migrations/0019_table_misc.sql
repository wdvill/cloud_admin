CREATE TABLE `misc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `misc_key` varchar(50) NOT NULL DEFAULT '',
  `value` varchar(1000) NOT NULL DEFAULT '',
  `description` varchar(200) NOT NULL DEFAULT '',
  `create_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `misc_key` (`misc_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

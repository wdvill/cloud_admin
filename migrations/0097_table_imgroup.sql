CREATE TABLE `imgroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contract_id` int NOT NULL DEFAULT 0,
  `im_group_id` int NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `contract_id` (`contract_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

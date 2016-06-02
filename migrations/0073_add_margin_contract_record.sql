CREATE TABLE `margin_contract_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `margin_record_id` int(11) NOT NULL DEFAULT '0',
  `contract_id` int(11) NOT NULL DEFAULT '0',
  `milestone_id` int(11) NOT NULL DEFAULT '0',
  `weekstone_id` int(11) NOT NULL DEFAULT '0',
  `order_id` int(11) NOT NULL DEFAULT '0',
  `create_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

alter table milestone add term int not null default 0;

alter table milestone add pay_order_id int not null default 0;

alter table milestone add index(pay_order_id);

CREATE TABLE `weekstone` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contract_id` int(11) NOT NULL DEFAULT '0',
  `amount` decimal(8,2) NOT NULL DEFAULT '0.00',
  `actual_amount` decimal(8,2) NOT NULL DEFAULT '0.00',
  `status` varchar(20) NOT NULL DEFAULT '',
  `order_id` int(11) NOT NULL DEFAULT '0',
  `pay_order_id` int(11) NOT NULL DEFAULT '0',
  `start_at` datetime DEFAULT NULL,
  `end_at` datetime DEFAULT NULL,
  `term` int(11) NOT NULL DEFAULT '0',
  `shot_times` int(11) NOT NULL DEFAULT '0',
  `create_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `contract_id` (`contract_id`),
  KEY `order_id` (`order_id`),
  KEY `pay_order_id` (`pay_order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `weekstone_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `weekstone_id` int(11) NOT NULL DEFAULT '0',
  `attachment_id` int(11) NOT NULL DEFAULT '0',
  `message` varchar(500) NOT NULL DEFAULT '',
  `rtype` varchar(20) NOT NULL DEFAULT '',
  `create_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `weekstone_id` (`weekstone_id`),
  KEY `attachment_id` (`attachment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `shotrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `weekstone_id` int(11) NOT NULL DEFAULT '0',
  `attachment_id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(50) NOT NULL DEFAULT '',
  `hour` int(11) NOT NULL DEFAULT '0',
  `shot_at` datetime NOT NULL,
  `activity` int(11) NOT NULL DEFAULT '0',
  `keyboard` int(11) NOT NULL DEFAULT '0',
  `mouse` int(11) NOT NULL DEFAULT '0',
  `description` varchar(500) NOT NULL DEFAULT '',
  `create_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `weekstone_id` (`weekstone_id`),
  KEY `attachment_id` (`attachment_id`),
  KEY `shot_at` (`shot_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

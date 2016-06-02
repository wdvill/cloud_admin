CREATE TABLE `weekstone_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `weekstone_id` int(11) NOT NULL DEFAULT '0',
  `audit_attachment_id` int(11) NOT NULL DEFAULT '0',
  `reason` varchar(500) NOT NULL DEFAULT '',
  `audit_at` datetime DEFAULT NULL,
  `create_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `weekstone_id` (`weekstone_id`),
  KEY `audit_attachment_id` (`audit_attachment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

alter table milestone_record add audit_at datetime default null;

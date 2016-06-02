alter table order_order add job_id int not null default 0;

alter table order_order add index(job_id);

alter table order_order add status varchar(20) not null default "";

alter table order_order add amount decimal(8,2) not null default '0';

alter table order_order add fee decimal(8,2) not null default '0';

alter table order_order add confirm_at datetime default null;

alter table order_order add order_type varchar(20) not null default "";

alter table milestone add order_id int not null default 0;

alter table contract add order_id int not null default 0;

alter table milestone drop actual_amount;

alter table milestone_record drop amount;


CREATE TABLE `payinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL DEFAULT '0',
  `order_id` int(11) NOT NULL DEFAULT '0',
  `card_no` varchar(20) NOT NULL DEFAULT '',
  `alipay` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `order_id` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

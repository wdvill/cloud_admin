alter table team add location_id int not null default 0;

alter table team add link varchar(100) not null default "";

alter table team add is_verify tinyint(1) not null default 0;


CREATE TABLE `team_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) NOT NULL DEFAULT '0',
  `logo` varchar(200) NOT NULL DEFAULT '',
  `overview` longtext NOT NULL,
  `address` varchar(100) NOT NULL DEFAULT '',
  `phone` varchar(20) NOT NULL DEFAULT '',
  `email` varchar(30) NOT NULL DEFAULT '',
  `contact` varchar(20) NOT NULL DEFAULT '',
  `contact_phone` varchar(20) NOT NULL DEFAULT '',
  `permit_number` varchar(30) NOT NULL DEFAULT '',
  `org_number` varchar(20) NOT NULL DEFAULT '',
  `permit_img` varchar(200) NOT NULL DEFAULT '',
  `org_img` varchar(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `team_id` (`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

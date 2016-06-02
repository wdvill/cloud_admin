alter table `user` add `identify` varchar(20) NOT NULL DEFAULT '';

alter table `profile` add `identify` varchar(20) NOT NULL DEFAULT '';
alter table `profile` add `is_notice` TINYINT NOT NULL DEFAULT 0;

alter table `verifycode` add `is_used` TINYINT NOT NULL DEFAULT 0;

alter table `verifycode` add `last_verity_time` DATETIME NULL;
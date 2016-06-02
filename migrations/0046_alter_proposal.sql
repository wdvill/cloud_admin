ALTER TABLE `proposal` DROP COLUMN `memo`;

ALTER TABLE `proposal` ADD COLUMN `attachment_id` INT(11) NOT NULL DEFAULT '0';

ALTER TABLE `proposal` ADD COLUMN `archive_c` tinyint(1) NOT NULL DEFAULT '0';

ALTER TABLE `proposal` ADD COLUMN `message` LONGTEXT;

ALTER TABLE `proposal` ADD COLUMN `reason` VARCHAR(500) NOT NULL DEFAULT "";

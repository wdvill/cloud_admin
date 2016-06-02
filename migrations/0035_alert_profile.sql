ALTER TABLE `profile` DROP COLUMN `country`;

ALTER TABLE `profile` DROP COLUMN `city`;

ALTER TABLE `profile` ADD COLUMN `location_id` INT(11) NOT NULL DEFAULT '0';


CREATE TABLE `system_user` (
  `id` int(10) UNSIGNED NOT NULL,
  `user` varchar(50) NOT NULL,
  `passwd` varchar(50) NOT NULL,
  `create_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE `system_user` CHANGE `id` `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT;

ALTER TABLE `system_user`
  ADD PRIMARY KEY (`id`);

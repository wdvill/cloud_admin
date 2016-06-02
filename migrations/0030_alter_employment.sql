alter table employment add role tinyint(2) NOT NULL DEFAULT '0';

alter table employment change column city city_id int(11) NOT NULL DEFAULT '0';
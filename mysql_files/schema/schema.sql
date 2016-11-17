CREATE DATABASE friend_match;

USE friend_match;

CREATE TABLE `user` (
  `user_id` BIGINT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(45) NULL,
  `user_email` VARCHAR(45) NULL,
  `user_password` VARCHAR(100) NULL,
  CONSTRAINT `pk_user_id` PRIMARY KEY (`user_id`));

  
CREATE TABLE `user_details` (
	`id` BIGINT NULL,
    `user_name` VARCHAR(45) NULL,
    `age` TINYINT NULL,
    `gender` CHAR(1) NULL,
    `city` VARCHAR(20) NULL,
    `location` VARCHAr(50) NULL,
    `phone_number` VARCHAR(20) NULL,
    CONSTRAINT `pk_user_details_id` PRIMARY KEY (`id`),
    CONSTRAINT `fk_user_details_id` FOREIGN KEY(`id`)
    REFERENCES `user`(`user_id`) ON DELETE CASCADE
);

CREATE TABLE `hobby` (
	`hobby_id` BIGINT NULL AUTO_INCREMENT,
    `hobby_name` VARCHAR(45) NULL,
    CONSTRAINT `pk_hobby_id` PRIMARY KEY(`hobby_id`)
);

CREATE TABLE `event` (
	`event_id` BIGINT NULL AUTO_INCREMENT,
    `event_name` VARCHAR(45) NULL,
    `event_city` VARCHAR(20) NULL,
    `event_date` DATE NULL,
    CONSTRAINT `pk_event_id` PRIMARY KEY(`event_id`)
);

CREATE TABLE `user_hobby` (
	`id` BIGINT NULL,
    `hobby_id` BIGINT NULL,
    CONSTRAINT `pk_user_hobby` PRIMARY KEY(`id`, `hobby_id`),
    CONSTRAINT `fk_user_hobby_user_id` FOREIGN KEY(`id`)
    REFERENCES `user`(`user_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_user_hobby_id` FOREIGN KEY(`hobby_id`)
    REFERENCES `hobby`(`hobby_id`) ON DELETE CASCADE
);

CREATE TABLE `user_event` (
	`id` BIGINT NULL,
    `event_id` BIGINT NULL,
    CONSTRAINT `pk_user_event` PRIMARY KEY(`id`, `event_id`),
    CONSTRAINT `fk_user_event_user_id` FOREIGN KEY(`id`)
    REFERENCES `user`(`user_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_user_event_id` FOREIGN KEY(`event_id`)
    REFERENCES `event`(`event_id`) ON DELETE CASCADE
);

CREATE TABLE `related_hobby` (
	`hobby_id` BIGINT NULL,
    `related_hobby_id` BIGINT NULL,
    CONSTRAINT `pk_related_hobby` PRIMARY KEY(`hobby_id`, `related_hobby_id`),
    CONSTRAINT `fk_hobby_id` FOREIGN KEY(`hobby_id`)
    REFERENCES `hobby`(`hobby_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_related_hobby_id` FOREIGN KEY(`related_hobby_id`)
    REFERENCES `hobby`(`hobby_id`) ON DELETE CASCADE
);

CREATE TABLE `event_interest_group` (
	`event_id` BIGINT NULL,
    `hobby_id` BIGINT NULL,
    CONSTRAINT `pk_event_interest_group` PRIMARY KEY(`event_id`, `hobby_id`),
    CONSTRAINT `fk_interest_group_event_id` FOREIGN KEY(`event_id`)
    REFERENCES `event`(`event_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_interest_group_hobby_id` FOREIGN KEY(`hobby_id`)
    REFERENCES `hobby`(`hobby_id`) ON DELETE CASCADE
);

CREATE TABLE `user_available_time` (
	`id` BIGINT NULL,
    `from_time` TIME NULL,
    `to_time` TIME NULL,
    CONSTRAINT `pk_user_available_time` PRIMARY KEY(`id`, `from_time`, `to_time`),
    CONSTRAINT `fk_user_available_time_id` FOREIGN KEY(`id`)
    REFERENCES `user`(`user_id`) ON DELETE CASCADE
);


CREATE TABLE `user_friend` (
	`id` BIGINT NULL,
    `friend_id` BIGINT NULL,
    CONSTRAINT `pk_user_friend` PRIMARY KEY(`id`, `friend_id`),
    CONSTRAINT `fk_user_friend_id` FOREIGN KEY(`id`)
    REFERENCES `user`(`user_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_user_friend_friend_id` FOREIGN KEY(`friend_id`)
    REFERENCES `user`(`user_id`) ON DELETE CASCADE
);
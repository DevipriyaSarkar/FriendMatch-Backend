CREATE DATABASE friend_match;

USE friend_match;

CREATE TABLE `user` (
  `user_id` BIGINT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(45) NULL,
  `user_username` VARCHAR(45) NULL,
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
	`hobby_name` VARCHAR(45) NULL,
    `related_hobby` VARCHAR(45) NULL,
    CONSTRAINT `pk_hobby` PRIMARY KEY(`hobby_name`, `related_hobby`)
);


CREATE TABLE `user_hobby` (
	`id` BIGINT NULL,
    `hobby` VARCHAR(45) NULL,
    CONSTRAINT `pk_user_hobby` PRIMARY KEY(`id`, `hobby`),
    CONSTRAINT `fk_user_hobby_user_id` FOREIGN KEY(`id`)
    REFERENCES `user`(`user_id`) ON DELETE CASCADE
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
DROP DATABASE IF EXISTS `epytodo`;
CREATE DATABASE IF NOT EXISTS `epytodo`;

USE epytodo;
CREATE TABLE IF NOT EXISTS `user` (
    `user_id` INT(11) AUTO_INCREMENT NOT NULL,
    `username` VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    PRIMARY KEY(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `task` (
    `quantity` INT(11) NOT NULL DEFAULT 0,
    `task_id` INT(11) AUTO_INCREMENT NOT NULL,
    `name` VARCHAR(255) NOT NULL DEFAULT 'name',
    `description` VARCHAR(255) NOT NULL DEFAULT 'description',
    `status` enum('not started', 'in progress', 'finished') NOT NULL DEFAULT 'not started',
    `begin` TIMESTAMP DEFAULT UTC_TIMESTAMP,
    `end` TIMESTAMP DEFAULT UTC_TIMESTAMP,
    PRIMARY KEY(`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `user_has_task` (
    `fk_user_id` INT(11) NOT NULL,
    `fk_task_id` INT(11) NOT NULL,
    foreign key (`fk_user_id`) references `user`(`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    foreign key (`fk_task_id`) references `task`(`task_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- 基于docker创建MySQL

-- 创建website数据库
CREATE DATABASE `website` DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;
-- 创建 Django Session 表
CREATE TABLE `website`.`django_session`
(
    `session_key`  varchar(40) NOT NULL,
    `session_data` longtext    NOT NULL,
    `expire_date`  datetime    NOT NULL,
    PRIMARY KEY (`session_key`),
    KEY `django_session_de54fa62` (`expire_date`)
) ENGINE = InnoDB COMMENT ='Django Session';


--







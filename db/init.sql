-- 基于docker创建MySQL

# -- MySQL57版本
# docker run -d -p 13357:3306 --name mysql5743 -e MYSQL_ROOT_PASSWORD=%aKyWJ9nesb2 mysql:5.7.43
# -- MySQL80版本
# docker run -d -p 13380:3306 --name mysql80 -e MYSQL_ROOT_PASSWORD=%aKyWJ9nesb2 mysql:latest

# mysql> select @@version;
# +-----------+
# | @@version |
# +-----------+
# | 8.0.34    | aliyun
# +-----------+
# 1 row in set (0.00 sec)

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

-- 创建用户表

-- 创建菜单表








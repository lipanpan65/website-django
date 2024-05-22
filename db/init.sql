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



-- 创建角色表
CREATE TABLE `dbms_user_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `role_name` varchar(128) NOT NULL COMMENT '名称',
  `role_type` smallint(255) NOT NULL DEFAULT '1' COMMENT '角色类型:user 0 admin 1',
  `status` smallint(255) NOT NULL DEFAULT '1' COMMENT '角色状态：1 启用,0 禁用',
  `create_user` varchar(128) DEFAULT NULL COMMENT '创建人',
  `update_user` varchar(128) DEFAULT NULL COMMENT '修改人',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='基础信息表-用户角色表'

-- 任务表
 CREATE TABLE `dbms_celery_task_main` (
  `id` bigint(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增键',
  `task_id` varchar(50) NOT NULL COMMENT 'celery的任务ID',
  `task_type` varchar(100) NOT NULL COMMENT '任务类型',
  `task_status` smallint(6) NOT NULL COMMENT '任务状态: 0_任务下发，100_执行结束',
  `task_result` smallint(6) DEFAULT NULL COMMENT '任务执行结果: 0_成功，大于0为失败',
  `op_user` varchar(50) DEFAULT NULL COMMENT '操作人',
  `task_args` mediumtext COMMENT '执行参数',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_task_id` (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='celery的任务表——主表';

-- 创建菜单表

CREATE TABLE `dbms_user2group` (
  `id` bigint(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `group_id` bigint(10) unsigned NOT NULL COMMENT '用户组表主键ID',
  `user_id` bigint(10) unsigned NOT NULL COMMENT '用户主键ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_group_id_user_id` (`group_id`,`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8 COMMENT='基础信息表-用户和用户组关系表'











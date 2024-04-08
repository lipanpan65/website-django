CREATE TABLE `tb_blog_article`
(
    `id`           int(11)      NOT NULL AUTO_INCREMENT COMMENT '自增主键',
    `status`       varchar(64)  NOT NULL DEFAULT 'draft' COMMENT '帖子状态：draft:草稿,publish:已发布',
    `title`        varchar(256) NOT NULL DEFAULT '无标题' COMMENT '帖子标题',
    `content`      longtext     NULL     DEFAULT NULL COMMENT '帖子内容',
    `content_html` longtext     NULL     DEFAULT NULL COMMENT '帖子内容的html',
    `create_user`  varchar(256) NULL     DEFAULT NULL COMMENT '创建人',
    `update_user`  varchar(256) NULL     DEFAULT NULL COMMENT '修改人',
    `create_time`  datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time`  datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci COMMENT ='专题-文章分类表';


-- 修改表结构


CREATE TABLE `dbms_userinfo`
(
    `id`          bigint(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增主键',
    `username`    varchar(50)         NOT NULL COMMENT '用户名',
    `name`        varchar(50)                  DEFAULT NULL COMMENT '姓名',
    `email`       varchar(50)                  DEFAULT NULL COMMENT '邮箱',
    `phone`       varchar(50)                  DEFAULT NULL COMMENT '联系电话',
    `status`      int(11)             NOT NULL DEFAULT '1' COMMENT '状态：1:启用，0:禁用',
    `role_id`     int(11)             NOT NULL COMMENT '角色ID',
    `org_name`        varchar(500)                 DEFAULT NULL COMMENT '组织架构',
    `org_id`       varchar(50)                  DEFAULT NULL COMMENT '组织架构ID',
    `create_time` datetime            NOT NULL COMMENT '创建时间',
    `create_user` varchar(100)                 DEFAULT NULL COMMENT '创建人',
    `update_time` datetime            NOT NULL COMMENT '更新时间',
    `update_user` varchar(100)                 DEFAULT NULL COMMENT '更新人',
    `note`        varchar(2000)                DEFAULT NULL COMMENT '备注',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uniq_username` (`username`),
    KEY `idx_username_email` (`name`, `email`),
    KEY `idx_email` (`email`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 12
  DEFAULT CHARSET = utf8 COMMENT ='基础信息表-用户基础信息表'



CREATE TABLE `tbl_blog_article`
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

-- 2019-3-11 wjc 创建数据库
CREATE DATABASE wlblog;

-- 2019-3-11 wjc 创建user表
create table tb_user(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(20) NULL DEFAULT NULL,
birth DATE NULL DEFAULT NULL,
sex INT NULL DEFAULT 1,
phone DECIMAL(11,0) NULL,
avatar_id INT NULL,
password VARCHAR(20) NOT NULL,
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0,
last_login DATETIME,
is_superuser INT DEFAULT 0,
username VARCHAR(20),
first_name VARCHAR(20),
last_name VARCHAR(20),
email VARCHAR(20),
is_staff VARCHAR(20),
is_active VARCHAR(20),
date_joined datetime
) AUTO_INCREMENT=1;

-- 2019-3-21 wjc 创建标签表
create table tb_tag(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
user_id INT NOT NULL,
tag VARCHAR(30),
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0) AUTO_INCREMENT=1;

-- 2019-3-21 wjc 创建博客文章表
create table tb_article(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
author INT NOT NULL,
title VARCHAR(30),
body TEXT,
is_secret INT DEFAULT 0,
liker INT,
unliker INT,
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0) AUTO_INCREMENT=1;

-- 2019-3-21 wjc 创建文章标签表
create table tb_article_tag(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
article INT NOT NULL,
tag_id INT NOT NULL,
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0) AUTO_INCREMENT=1;

-- 2019-3-21 wjc 创建草稿表
create table tb_article_draft(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
author_id INT NOT NULL,
title VARCHAR(30),
body TEXT,
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0) AUTO_INCREMENT=1;

-- 2019-3-21 wjc 创建整合集表
create table tb_collation_set(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
user_id INT NOT NULL,
first_title VARCHAR(30),
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0) AUTO_INCREMENT=1;

-- 2019-3-21 wjc 创建整合集二级标题和内容表
create table tb_collation_set_body(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
collation_set_id INT NOT NULL,
second_title VARCHAR(30),
body TEXT,
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0) AUTO_INCREMENT=1;

-- 2019-3-27 wjc 在user表中添加简介（Introduction）字段
ALTER TABLE tb_user
ADD COLUMN Introduction VARCHAR(200) NULL;

-- 2019-3-28 WJC 修改文章表的author字段为author_id
ALTER TABLE tb_article CHANGE author author_id INT NOT NULL;

-- 2019-3-28 wjc 修改文章标签表的article字段为article_id
ALTER TABLE tb_article_tag CHANGE article article_id INT NOT NULL;

-- 2019-3-29 wjc 创建评论表
create table tb_comments(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
article_id INT NOT NULL,
commentator_id INT NOT NULL,
commentee_id INT NOT NULL,
comment_body VARCHAR(2000),
category INT NOT NULL,
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0) AUTO_INCREMENT=1;

-- 2019-3-29 wjc 创建回复表
create table tb_reply(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
comment_id INT NOT NULL,
replier_id INT NOT NULL,
respondent_id INT NOT NULL,
reply_body VARCHAR(2000),
category INT NOT NULL,
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0) AUTO_INCREMENT=1;

-- 2019-3-31 wjc 创建点赞表
create table tb_click_like(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
click_liker_id INT NOT NULL,
article_id INT NOT NULL,
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0) AUTO_INCREMENT=1;

-- 2019-4-2 wjc 创建收藏表
create table tb_collection(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
user_id INT NOT NULL,
article_id INT NOT NULL,
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0) AUTO_INCREMENT=1;

-- 2019-4-3 wjc 创建用户信息表
create table tb_user_information(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
user_id INT NOT NULL,
summary VARCHAR(2000) NULL DEFAULT NULL,
school VARCHAR(100) NULL DEFAULT NULL,
address VARCHAR(100) NULL DEFAULT NULL,
github VARCHAR(500) NULL DEFAULT NULL,
interests VARCHAR(500) NULL DEFAULT NULL,
skill VARCHAR(500) NULL DEFAULT NULL,
email VARCHAR(500) NULL DEFAULT NULL,
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0) AUTO_INCREMENT=1;

-- 2019-4-5 wjc 创建关注表
create table tb_attention(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
follower_id INT NOT NULL,
attentor_id INT NOT NULL,
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0) AUTO_INCREMENT=1;

-- 2019-4-5 wjc 创建留言表
create table tb_user_leave(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
leaver_id INT NOT NULL,
leaved_person_id INT NOT NULL,
leave_body VARCHAR(2000),
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0) AUTO_INCREMENT=1;

-- 2019-4-5 wjc 在留言表中添加是否已读字段
ALTER TABLE tb_user_leave
ADD COLUMN is_read INT DEFAULT 0;

-- 2019-4-6 wjc 创建消息表
create table tb_message(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
user_id INT NOT NULL,
category INT NOT NULL,
message_body VARCHAR(2000),
leave_msg_id INT NULL DEFAULT NULL,
article_id INT NULL DEFAULT NULL,
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0) AUTO_INCREMENT=1;

-- 2019-4-6 wjc 在消息表中添加是否已读字段
ALTER TABLE tb_message
ADD COLUMN is_read INT DEFAULT 0;

-- 2019-4-11 wjc 创建头像表
create table tb_avatar_img(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
avatar VARCHAR(2000),
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0) AUTO_INCREMENT=1;

-- 2019-4-14 wjc 创建相册表
create table tb_photo(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
user_id INT NOT NULL,
photo_name VARCHAR(200),
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0) AUTO_INCREMENT=1;

-- 2019-4-14 wjc 创建相册图片表
create table tb_photo_img(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
photo_id INT NOT NULL,
title VARCHAR(200),
img_url VARCHAR(200),
description VARCHAR(500) NULL DEFAULT NULL,
created DATETIME,
updated DATETIME,
deleted INT DEFAULT 0) AUTO_INCREMENT=1;

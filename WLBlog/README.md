## 前言
这个博客系统，是我在公司实习之后，独立完成的一个比较完善的博客系统。一个用于毕业设计的博客项目，之前学了学了Django框架做个一个简易的博客系统，当时是为了熟悉Django框架，这个项目是为了完成之前就定下的目标，做一个完整的博客供自己使用。

## 个人博客系统
使用工具和开发环境：windows7/pycharm/django 2.1/Vue.js
## 主要功能：
- 文章，页面，栏目分类，标签的添加，删除，编辑等。文章及页面支持`Markdown`。
- 文章搜索功能（输入关键字，搜索相关文章）。
- 完整的评论功能，包括发表回复评论。
- 侧边栏功能，最新文章，最热文章。
- 个人相册。
- 消息阅读，消息提醒。

### 配置
配置都是在`setting.py`中.部分配置迁移到了后台配置中。
redis的配置
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

## 数据迁移
终端下执行:

    ./manage.py makemigrations
    ./manage.py migrate
### 创建超级用户

 终端下执行:

    ./manage.py createsuperuser
### 创建测试数据
终端下执行:

    ./manage.py create_testdata
### 开始运行：

  cmd执行`redis-server`
  
 `python manage.py runserver`





 浏览器打开: http://127.0.0.1:8000/home  就可以看到效果了。

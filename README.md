## 个人博客系统
使用工具和开发环境：windows7/pycharm/django 2.0
## 主要功能：
- 文章，页面，栏目分类，标签的添加，删除，编辑等。文章及页面支持`Markdown`。
- 完整的评论功能，包括发表回复评论。
- 侧边栏功能，最新文章，最热文章。

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
 执行：
 `./manage.py runserver`





 浏览器打开: http://127.0.0.1:8000/  就可以看到效果了。

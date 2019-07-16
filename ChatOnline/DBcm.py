from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy     # 操作数据库的扩展包
from flask_script import Manager        # 用命令操作的扩展包
from flask_migrate import MigrateCommand, Migrate       # 操作数据库迁移文件的扩展包

app = Flask(__name__)
# 数据库信息设置
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@127.0.0.1:3306/chatonline"
# 动态追踪修改设置，如未设置只会提示警告，极大影响mysql性能(Flask-SQLAlchemy版本必须小于2.2，高版本已经修改了)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
manager = Manager(app)
# 创建迁移对象
migrate = Migrate(app, db)
# 将迁移文件的命令添加到"db"中
manager.add_command('db', MigrateCommand)


# 创建模型
# 用户表
class User(db.Model, UserMixin):
    """用户"""
    __tablename__ = "tb_user"   # 表名
    __table_args__ = {"mysql_engine": "InnoDB"}     # 支持事务操作和外键

    id = db.Column(db.Integer, doc="用户id", primary_key=True, unique=True)
    username = db.Column(db.String(20), doc="用户名")
    password = db.Column(db.String(200), doc="密码", nullable=False)
    phone = db.Column(db.String(20), doc="手机", nullable=False)
    is_superuser = db.Column(db.Boolean, doc="是否为管理员", default=False)


if __name__ == "__main__":
    # app.debug = True
    manager.run()


# 迁移命令如下
"""
比如上面的代码所在的文件名称为DBcm.py。

1.python DBcm.py db init   　生成管理迁移文件的migrations目录

2.python DBcm.py db migrate -m "注释"　　 在migrations/versions中生成一个文件，该文件记录数据表的创建和更新的不同版本的代码。

3.python DBcm.py db upgrade　　在数据库中生成对应的表格。

4.当需要改表格的时候，改完先执行第二步，然后再执行第三步。

5.需要修改数据表的版本号的时候需要做的操作如下：

python DBcm.py db upgrade 版本号　　向上修改版本号

python DBcm.py db downgrade 版本号 　　向下修改版本号

可能用到的其他的语句：

python DBcm.py db history  　　查看历史版本号

python DBcm.py db current 　　查看当前版本号
"""

"""
# 删除所有的表
db.drop_all()

# 创建表
db.create_all()

注意，以上两句话可能与app.debug = True冲突，因为表若修改，
文件就会运行了，数据库里边已经有了数据，后面再运行就可能报错
"""

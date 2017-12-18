import os
from app import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand


# 获取配置参数名
config_name = os.environ.get('FLASK_CONFIG') or 'default'
# 根据配置参数名，创建Flask实例
app = create_app(config_name)
# 添加命令行控制
manager = Manager(app)

# 添加数据库迁移命令到终端
manager.add_command('db', MigrateCommand)


# 启动应用程序
if __name__ == '__main__':
    manager.run()

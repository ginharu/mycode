from flask import Flask, render_template
from app.config import config
from app.extensions import config_extensions
from app.views import config_blueprint


# 封装一个对外公开的方法，专门用于创建Flask对象
def create_app(config_name):
    # 创建应用实例
    app = Flask(__name__)
    # 初始化配置
    app.config.from_object(config[config_name])
    # 调用初始化函数
    config[config_name].init_app(app)
    # 初始化各种扩展
    config_extensions(app)
    # 配置蓝本
    config_blueprint(app)
    # 配置错误显示
    config_errorhandler(app)
    # 返回应用实例
    return app


def config_errorhandler(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html')

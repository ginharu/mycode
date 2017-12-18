import os
import pymysql
pymysql.install_as_MySQLdb()
base_dir = os.path.abspath(os.path.dirname(__file__))


# 配置基类
class Config:
    # 秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'
    # 数据库
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 邮件发送
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.163.com'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'yuanjl_yuka@163.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'yuka1223'
    MAIL_PORT = os.environ.get("ddd") or 465
    MAIL_USE_SSL = True

    # 上传文件的大小，默认不限制
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    # 配置上传文件保存目录
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'static/upload')

    # 额外的初始化操作
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:yuka1223@localhost:3306/flaskblog'


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:yuka1223@localhost:3306/flaskblog'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:yuka1223@localhost:3306/flaskblog'


# 对外公开的配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

from .reply import reply
from .main import main
from .user import user


# 蓝本配置
DEFAULT_BLUEPRINT = (
    # 蓝本，url前缀
    (main, ''),
    (user, '/user'),
    (reply,'/reply')
)


# 注册蓝本
def config_blueprint(app):
    for blue_print, url_prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blue_print, url_prefix=url_prefix)

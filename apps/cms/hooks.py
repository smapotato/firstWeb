# 定义一些功能型函数
from .views import bp
from flask import session, g
from .models import CMSUser
import config
from .models import CMSUser,CMSPersmission


@bp.before_request
def before_request():  # 在执行视图函数之前，取出登录的用户
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user

@bp.context_processor
def cms_context_processor():#返回的字典中的键可以在模板上下文中使用
    return {"CMSPermission":CMSPersmission}
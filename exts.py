# 防止app和数据库相互引用
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

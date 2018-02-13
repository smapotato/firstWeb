import os

# SECRET_KEY = os.urandom(24)
SECRET_KEY = "fdadfnjiesc"
DEBUG = True
TEMPLATES_AUTO_RELOAD = True  # 模板自动加载
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'firstWeb'
USERNAME = 'root'
PASSWORD = '960825qq'

# dialect+driver://username:password@host:port/database
DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,
                                                                                        password=PASSWORD,
                                                                                        host=HOSTNAME, port=PORT,
                                                                                        db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
CMS_USER_ID = "DFASDFDC"
FRONT_USER_ID = "fdfwef4165"
# 发送者邮箱的服务器配置
MAIL_SERVER = "smtp.163.com"
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USE_SSL = False
# MAIL_DEBUG : 默认为 app.debug
MAIL_USERNAME = "15702431853@163.com"
MAIL_PASSWORD = "xsy960825"
MAIL_DEFAULT_SENDER = "15702431853@163.com"
# MAIL_MAX_EMAILS : 默认为 None
# MAIL_SUPPRESS_SEND : 默认为 app.testing
# MAIL_ASCII_ATTACHMENTS : 默认为 False

# encoding: utf-8
import os

UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'images')

# # ueditor的相关配置
# UEDITOR_UPLOAD_TO_QINIU = True
# UEDITOR_QINIU_ACCESS_KEY = "M4zCEW4f9XPanbMN-Lb9O0S8j893f0e1ezAohFVL"
# UEDITOR_QINIU_SECRET_KEY = "7BKV7HeEKM3NDJk8_l_C89JI3SMmeUlAIatzl9d4"
# UEDITOR_QINIU_BUCKET_NAME = "hyvideo"
# UEDITOR_QINIU_DOMAIN = 'http://7xqenu.com1.z0.glb.clouddn.com'

# flask-paginate的相关配置
PER_PAGE = 10

# celery相关的配置
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
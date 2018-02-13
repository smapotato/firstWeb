from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class CMSPersmission(object):
    # 255的二进制方式表示 1111 1111
    ALL_PERMISSION = 0b11111111
    # 1 访问者权限
    VISITOR = 0b00000001
    # 2 管理帖子权限
    POSTER = 0b00000010
    # 3 管理评论的权限
    COMMENTER = 0b00000100
    # 4 管理版块的权限
    BOARDER = 0b00001000
    # 5  管理前台用户的权限
    FRONTUSER = 0b00010000
    # 6 管理后台用户的权限
    CMSUSER = 0b00100000
    # 7 管理后台管理员的权限
    ADMINER = 0b01000000


cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True)
)


class CMSRole(db.Model):  # 角色与用户之间多对多关系
    __tablename__ = "cms_role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, default=CMSPersmission.VISITOR)

    users = db.relationship('CMSUser', secondary=cms_role_user, backref="roles")


class CMSUser(db.Model):  # SQLAlchemy 会自动帮我们创建构造器, 并且所有定义的字段名将会成为此构造器的关键字参数名
    __tablename__ = "cms_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):  # 密码加密，需重新构造
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):  # 加密 user.password = "abc"
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):  # 检查密码是否一致
        result = check_password_hash(self.password, raw_password)
        return result

    @property
    def permissions(self):#查询用户的权限
        if not self.roles:
            return 0
        all_permissions = 0
        for role in self.roles:
            permissions = role.permissions
            all_permissions |= permissions  # 或操作加上所有的权限
        return all_permissions

    def has_permission(self, permission):
        return self.permissions&permission == permission # 判断用户是否有权限

    @property
    def is_developer(self):
        return self.has_permission(CMSPersmission.ALL_PERMISSION)

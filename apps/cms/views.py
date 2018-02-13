from flask import Blueprint, views, render_template, request, session, \
    redirect, url_for, g, jsonify
from .forms import LoginForm, ResetpwdForm, ResetEmailForm, AddBannerForm, UpdateBannerForm, AddBoardForm, \
    UpdateBoardForm
from .models import CMSUser, CMSPersmission
from .decorators import login_required, permission_required
import config, string, random
from exts import db, mail
from utils import restful, zlcache
from flask_mail import Message
from ..models import BannerModel, BoardModel, PostModel, HighlightPostModel
from tasks import send_mail
bp = Blueprint("cms", __name__, url_prefix="/cms")


@bp.route("/banners/")
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template("cms/cms_banner.html", banners=banners)


@bp.route("/abanner/", methods=["POST"])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority
        =priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_errors())


@bp.route('/ubanner/', methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图！')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dbanner/', methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请传入轮播图id！')

    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图！')

    db.session.delete(banner)
    db.session.commit()
    return restful.success()


@bp.route("/")
@login_required  # 登录限制，需要登录后才能访问首页
def index():  # 首页
    return render_template("cms/cms_index.html")


@bp.route("/profile/")
@login_required
def profile():  # 个人资料
    return render_template("cms/cms_profile.html")


@bp.route("/logout/")
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for("cms.login"))


@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error('请传递邮箱参数')
    source = list(string.ascii_letters)
    source.extend(map(lambda x: str(x), range(10)))
    captcha = "".join(random.sample(source, 6))
    message = Message("Python邮箱验证码", recipients=[email], body="你的验证码是:%s" % captcha)
    # 给邮箱发送邮件
    try:
        mail.send(message)
    except:
        return restful.server_error()
    # send_mail.delay("Python邮箱验证码",[email],"你的验证码是:%s" % captcha)
    zlcache.set(email, captcha)
    print(zlcache.get(email))
    return restful.success()


@bp.route("/posts/")  # 帖子管理
@login_required
@permission_required(CMSPersmission.POSTER)
def posts():
    context = {
        "posts": PostModel.query.all()
    }
    return render_template("cms/cms_posts.html",**context)


@bp.route("/hpost/", methods=["POST"])
@login_required
@permission_required(CMSPersmission.POSTER)
def hpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error("请传入帖子id")
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子")
    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


@bp.route("/uhpost/", methods=["POST"])
@login_required
@permission_required(CMSPersmission.POSTER)
def uhpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error("请传入帖子id")
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子")
    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


@bp.route("/comments/")  # 评论管理
@login_required
@permission_required(CMSPersmission.COMMENTER)
def comments():
    return render_template("cms/cms_comments.html")


@bp.route("/boards/")  # 板块管理
@login_required
@permission_required(CMSPersmission.BOARDER)
def boards():
    board_models = BoardModel.query.all()
    context = {"boards": board_models}
    return render_template("cms/cms_boards.html", **context)


@bp.route("/aboard/", methods=["POST"])
@login_required
@permission_required(CMSPersmission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_errors())


@bp.route("/uboard/", methods=["POST"])
@login_required
@permission_required(CMSPersmission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message="没有这个板块")
    else:
        return restful.params_error(message=form.get_errors())


@bp.route("/dboard/", methods=["POST"])
@login_required
@permission_required(CMSPersmission.BOARDER)
def dboard():
    board_id = request.form.get("board_id")
    if not board_id:
        return restful.params_error("请传入板块id")
    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error(message="没有这个板块")
    db.session.delete(board)
    db.session.commit()
    return restful.success()


@bp.route("/fusers/")  # 前台用户管理
@login_required
@permission_required(CMSPersmission.FRONTUSER)
def fusers():
    return render_template("cms/cms_fusers.html")


@bp.route("/cusers/")  # CMS用户管理
@login_required
@permission_required(CMSPersmission.CMSUSER)
def cusers():
    return render_template("cms/cms_cusers.html")


@bp.route("/croles/")  # 组管理
@login_required
@permission_required(CMSPersmission.ALL_PERMISSION)
def croles():
    return render_template("cms/cms_croles.html")


class LoginView(views.MethodView):  # 登录视图
    def get(self, message=None):
        return render_template("cms/cms_login.html", message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    # 如果设置session.permanent=True
                    # 那么过期时间是31天
                    session.permanent = True
                return redirect(url_for("cms.index"))
            else:
                return self.get(message="邮箱或密码错误")
        else:
            message = form.get_errors()  # form.errors.popitem()[1][0]
            # print(form.errors)
            return self.get(message=message)


class ResetPwdView(views.MethodView):  # 重置密码
    decorators = [login_required]

    def get(self):
        return render_template("cms/cms_resetpwd.html")

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # 返回json数据
                # return jsonify({ "code":200,"message":"" })
                return restful.success()
            else:
                # return jsonify({ "code":400,"message":"旧密码错误" })
                # return restful.params_error("旧密码错误")
                return restful.params_error(form.get_errors())

        else:
            # message = form.get_errors()
            # return jsonify({ "code":400,"message":message})
            return restful.params_error(form.get_errors())


class ResetEmailView(views.MethodView):  # 重置邮箱
    decorators = [login_required]

    def get(self):
        return render_template("cms/cms_resetemail.html")

    def post(self):
        form = ResetEmailForm(request.form)
        print(form.email.data)
        print(form.captcha.data)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_errors())


bp.add_url_rule("/login/", view_func=LoginView.as_view("login"))
bp.add_url_rule("/resetpwd/", view_func=ResetPwdView.as_view("resetpwd"))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))

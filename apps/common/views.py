from flask import Blueprint, views, render_template, make_response, jsonify
from io import BytesIO
from utils.captcha import Captcha
from utils import zlcache
import qiniu

bp = Blueprint("common", __name__, url_prefix="/common")


@bp.route("/")
def index():
    return "common index"


# @bp.route('/sms_captcha/',methods=['POST'])
# def sms_captcha():
#     form = SMSCaptchaForm(request.form)
#     if form.validate():
#         telephone = form.telephone.data
#         captcha = Captcha.gene_text(number=4)
#         print('发送的短信验证码是：',captcha)
#         if alidayu.send_sms(telephone,code=captcha):
#             zlcache.set(telephone,captcha)
#             return restful.success()
#         else:
#             # return restful.params_error()
#             zlcache.set(telephone,captcha)
#             return restful.success()
#     else:
#         return restful.params_error(message='参数错误！')



@bp.route("/captcha/")
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    zlcache.set(text, text)
    out = BytesIO()
    image.save(out, "png")
    out.seek(0)
    res = make_response(out.read())
    res.content_type = "image/png"
    return res

@bp.route("/uptoken")
def uptoken():
    access_key = "#"
    secret_key = "#"
    q = qiniu.Auth(access_key,secret_key)
    bucket = "存储空间名字"
    token = q.upload_token(bucket)
    return jsonify({"uptoken":token})
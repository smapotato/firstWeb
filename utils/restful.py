from flask import jsonify


class Httpcode(object):
    ok = 200
    paramserror = 400
    unautherror = 401
    servererror = 500


def restful_result(code, message, data):
    return jsonify({"code": code, "message": message, "data": data or {}})


def success(message="", data=None):
    return restful_result(code=Httpcode.ok, message=message, data=data)


def unauth_error(message=""):
    return restful_result(code=Httpcode.unautherror, message=message, data=None)


def params_error(message=""):
    return restful_result(code=Httpcode.paramserror, message=message, data=None)


def server_error(message=""):
    return restful_result(code=Httpcode.servererror, message=message or "服务器内部错误", data=None)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import datetime
import random

from common import utils
from models.sms import VerifyCode
from models.user import User
from .baiwutong import BaiWuTong


def verify_code(phone, code):
    vcode = VerifyCode.select().where(VerifyCode.phone == phone).first()
    if not vcode:
        return {"error_code":20031, "msg":"verify code not exists"}

    if vcode.vcount >= 3:
        return {"error_code":20033, "msg":"verify large than 3 times"}

    if vcode.code != code:
        vcode.vcount += 1
        vcode.save()
        return {"error_code":20032, "msg":"verify invalid"}

    now = utils.now()
    if (now - vcode.last_verity_time) >= datetime.timedelta(minutes=5):
        return {"error_code":20034, "msg":"verify is expires"}

    if vcode.is_used:
        return {"error_code":20035, "msg":"verify is used"}

    vcode.is_used = True
    vcode.vcount = 0
    vcode.save()
    return {"error_code":0, "msg":"ok"}


def send_code(phone, code=None):
    if not phone:
        return {"error_code": 20037, "msg": "phone not exists"}

    vcode = VerifyCode.select().where(VerifyCode.phone == phone).first()
    if not vcode:
        vcode = VerifyCode()

    if not code:
        code = random.randint(100000, 999999)

    baiwu = BaiWuTong()
    flag, msg = baiwu.send(phone=phone, text=msg_template_code(code))
    if not flag:
        return {"error_code": 20036, "msg": "send verify code failed"}

    now = utils.now()

    vcode.phone = phone
    vcode.code = code
    vcode.send_at = now
    vcode.vcount = 0
    vcode.is_used = False
    vcode.last_verity_time = now
    vcode.create_at = now
    vcode.save()

    return {"error_code":0, "msg":"ok", "vcode":code}


def send_verify_code(user, params):
    phone = params.get('phone')
    vtype = params.get("vtype")
    if not vtype or vtype not in ("enter", "register", "forget"):
        return {"error_code": 20631, "msg": "vtype invalid"}

    if vtype == "enter":
        # 为当前登录用户获取验证码
        if not user:
            return {"error_code": 20632, "msg": "user not exists"}
        return send_code(phone=user.phone)
    elif vtype in ("register", "forget", ):
        # register: 注册获取验证码
        # forget: 忘记密码获取验证码
        if not phone:
            return {"error_code": 20636, "msg": "username or phone not exists"}

        user = User.select().where(User.username == phone).first()
        if vtype == "register":
            if user:
                return {"error_code": 20633, "msg": "user phone already register"}
        if vtype == "forget":
            if not user:
                return {"error_code": 20634, "msg": "user not exists"}

        return send_code(phone=phone)


def msg_template_code(code):
    return u"您的短信验证码是:%s本短信5分钟内有效。[北京云族佳科技有限公司]" % code

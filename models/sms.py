# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from peewee import CharField, DateTimeField, IntegerField, BooleanField
from .base import BaseModel
from common import utils


class SmsRecord(BaseModel):
    phone = CharField(verbose_name="手机号", max_length=20, null=False)
    content = CharField(verbose_name="短信内容", max_length=255, null=False)
    status = CharField(verbose_name="发送状态", max_length=10, null=False)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

    class Meta:
        db_table = "sms_record"

class VerifyCode(BaseModel):
    phone = CharField(verbose_name="手机号", max_length=20, null=False)
    code = CharField(verbose_name="验证码", max_length=10, null=False)
    send_at = DateTimeField(verbose_name="发送时间", null=False, default=utils.now)
    vcount = IntegerField(verbose_name="验证次数", null=False, default=0)
    is_used = BooleanField(verbose_name="是否使用", null=False, default=False)
    last_verity_time = DateTimeField(verbose_name="最后一次验证时间", null=True)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

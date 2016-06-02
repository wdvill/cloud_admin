#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from peewee import CharField, IntegerField, FixedCharField, DateTimeField, ForeignKeyField
from .base import BaseModel
from .user import User
from common import utils

class Attachment(BaseModel):
    name = CharField(verbose_name="附件名称", max_length=250, null=False, default="")
    size = IntegerField(verbose_name="大小", null=False, default=0)
    path = CharField(verbose_name="路径", max_length=250, null=False, default="")
    md5 = FixedCharField(verbose_name="md5", max_length=32, null=False, default="")
    atype = CharField(verbose_name="附件类型", max_length=20, null=False, default="job")
    user = ForeignKeyField(User, null=False, default=0)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

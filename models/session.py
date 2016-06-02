#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from peewee import ForeignKeyField, CharField, DateTimeField
from .base import BaseModel
from .system import SystemUser
from common import utils

class Session(BaseModel):
    user = ForeignKeyField(SystemUser)
    session_key = CharField(verbose_name="sessionid", max_length=40, null=False, default="")
    device = CharField(verbose_name="device", max_length=20, null=False, default="")
    expire_at = DateTimeField(verbose_name="过期时间", null=False, default=utils.now)

    class Meta:
        auto_increment = False
        primary_key = False

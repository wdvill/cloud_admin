# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from peewee import CharField, DateTimeField, IntegerField, ForeignKeyField
from .base import BaseModel
from .user import User
from .team import Team
from common import utils


class Favorite(BaseModel):
    user = ForeignKeyField(User)
    team = ForeignKeyField(Team, null=False, default=0)
    target_id = IntegerField(verbose_name="收藏的对象id", null=False, default=0)
    # 需求者收藏：REQ，开发者收藏：DEV
    ftype = CharField(verbose_name="收藏类型", max_length=20, default="", help_text="需求方收藏服务方，服务方收藏工作")
    memo = CharField(verbose_name="收藏备注", max_length=100, default="")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

class Subscribe(BaseModel):
    user = ForeignKeyField(User)
    name = CharField(verbose_name="订阅名称", max_length=20, default="")
    keyword = CharField(verbose_name="搜索条件(json)", max_length=200, default="")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from peewee import ForeignKeyField, CharField, DateTimeField, IntegerField
from .base import BaseModel
from .user import User
from .team import Team
from .contract import Contract
from .proposal import Proposal
from common import utils

class Friend(BaseModel):
    user = ForeignKeyField(User, related_name="friend", help_text="只能是开发者")
    team = ForeignKeyField(Team, null=False, help_text="只能是需求者")
    #friend = ForeignKeyField(User, related_name="friend_user")
    ftype = CharField(verbose_name="谁的好友", max_length=10, null=False, default="", help_text="f, c")
    status = CharField(verbose_name="状态", max_length=20, null=False, default="normal")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

class IMGroup(BaseModel):
    contract = ForeignKeyField(Contract)
    proposal = ForeignKeyField(Proposal)
    im_group_id = IntegerField(verbose_name="im侧群id", null=False, default=0)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

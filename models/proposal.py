# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from peewee import CharField, DateTimeField, IntegerField, ForeignKeyField, TextField, DecimalField, BooleanField
from .base import BaseModel
from .contract import Contract
from .user import User
from .job import Job
from .team import Team
from .attachment import Attachment
from .question import Question
from common import utils


class Proposal(BaseModel):
    user = ForeignKeyField(User)
    job = ForeignKeyField(Job)
    invite = ForeignKeyField(User, help_text="邀请方", related_name="invite")
    team = ForeignKeyField(Team)
    ptype = CharField(verbose_name="提案类型, I 邀请，D 投标", max_length=10, null=False, default="D")
    status = CharField(verbose_name="提案状态", max_length=20, null=False, default="", help_text="active, refuse, revoke, interview, hire, archive")
    price = DecimalField(verbose_name="报价", max_digits=8, decimal_places=2, null=False, default=0)
    duration = IntegerField(verbose_name="预计完成时间", null=False, default=0)
    message = TextField(verbose_name="备注信息", null=True, default="")
    question = ForeignKeyField(Question)
    reason = CharField(verbose_name="拒绝撤销原因", max_length=500, null=False, default="")
    attachment = ForeignKeyField(Attachment, null=True, default=0)
    archive_c = BooleanField(verbose_name="需求者归档", null=False, default=False)
    update_at = DateTimeField(verbose_name="更新时间", null=False, default=utils.now)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
    day_reply = BooleanField(verbose_name="被邀请是否当天回复", null=False, default=False)
    contract = ForeignKeyField(Contract, null=True, default=0)
    is_view = BooleanField(verbose_name="需求者是否查看", null=False, default=False)


class ProposalMessage(BaseModel):
    user = ForeignKeyField(User, null=True)
    team = ForeignKeyField(Team, null=True)
    topic = CharField(verbose_name="话题", max_length=30, null=False, default="")
    content = TextField(verbose_name="回复内容", null=True, default="")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

    class Meta:
        db_table = "proposal_message"

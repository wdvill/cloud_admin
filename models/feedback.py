#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from peewee import CharField, DateTimeField, IntegerField, TextField, ForeignKeyField
from .base import BaseModel
from .user import User
from .team import Team
from .contract import Contract
from .question import Question
from common import utils

class Feedback(BaseModel):
    user = ForeignKeyField(User)
    team = ForeignKeyField(Team)
    ftype = CharField(verbose_name="反馈类型", max_length=20, null=False, default="", help_text="bug, suggest, signin_slow, run_slow, message_slow, unusual, exit")
    score = IntegerField(verbose_name="反馈评分", null=False, default=0)
    contract = CharField(verbose_name="联系方式", max_length=50, null=False, default="", help_text="手机号或邮箱")
    content = TextField(verbose_name="反馈内容", null=False, default="")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

# 结束合同给平台反馈
class FeedbackContract(BaseModel):
    contract = ForeignKeyField(Contract)
    question = ForeignKeyField(Question)
    user = ForeignKeyField(User)
    team = ForeignKeyField(Team)
    score = IntegerField(verbose_name="推荐率", null=False, default=0)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
    class Meta:
        db_table = "feedback_contract"

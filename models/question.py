# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from peewee import CharField, IntegerField, DateTimeField
from .base import BaseModel
from common import utils


class Question(BaseModel):
    name = CharField(verbose_name="问题名称", max_length=100, null=False)
    ename = CharField(verbose_name="英文名称", max_length=100, null=False)
    level = IntegerField(verbose_name="级别", null=False, default=0, help_text="越大越优先显示")
    qtype = CharField(verbose_name="问题类型", max_length=20, null=False, default="", 
                    help_text="user, proposal_revoke_f,proposal_refuse_f,proposal_refuse_c, contract_refuse, contract_revoke, contract_finish_f, contract_finish_c")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
